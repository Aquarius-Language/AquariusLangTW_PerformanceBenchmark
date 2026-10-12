using System.Diagnostics;
using System.Globalization;
using System.Security.Cryptography;
using System.Text.Json;
using AquariusLang.Object;
using AquariusLang.runtime;
using AquariusLang.Wasm;
using AquariusLang.Desktop.runtime;

CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
if (args.Length != 4) throw new ArgumentException("Usage: ParityProfile benchmark-root baseline.json typed-probes.wasm output.json");
var root = Path.GetFullPath(args[0]);
using var baseline = JsonDocument.Parse(File.ReadAllText(args[1]));
var results = new Dictionary<string, object>();
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
foreach (var spec in baseline.RootElement.GetProperty("benchmarks").EnumerateObject())
{
    string name = spec.Name;
    var sourcePath = Path.Combine(root, "benchmarks", "aquarius", name + ".aqua");
    var program = new WasmCompiler().Compile(File.ReadAllText(sourcePath));
    var output = new List<string>();
    var builtins = new Builtins();
    builtins.BuiltinFuncs["印出"] = new BuiltinObj(values => {
        output.Add(string.Join(" ", values.Select(v => v.Inspect())));
        return null!;
    });
    builtins.BuiltinFuncs["加入"] = BuiltinObj.FromPortable(4, _ => throw new InvalidOperationException("Host append used."));
    builtins.BuiltinFuncs["長度"] = BuiltinObj.FromPortable(1, _ => throw new InvalidOperationException("Host length used."));
    double expected = spec.Value.GetProperty("expected").GetDouble();
    void Validate(IObject? value)
    {
        if (value is ErrorObj error) throw new InvalidOperationException(error.Message);
        if (output.Count != 2 || !output[0].StartsWith("RESULT ") || !output[1].StartsWith("ELAPSED_MS "))
            throw new InvalidOperationException("Invalid output protocol.");
        double actual = double.Parse(output[0][7..]);
        double tolerance = spec.Value.TryGetProperty("relative_tolerance", out var relative)
            ? Math.Max(spec.Value.GetProperty("absolute_tolerance").GetDouble(), Math.Abs(expected) * relative.GetDouble()) : 0;
        if (!double.IsFinite(actual) || Math.Abs(actual - expected) > tolerance) throw new InvalidOperationException($"Incorrect {name}: {actual}, expected {expected}");
        if (!(double.Parse(output[1][11..]) > 0)) throw new InvalidOperationException("Invalid clock.");
    }
    using var runtime = new WasmRuntime(builtins, new WasmtimeEngine());
    for (int i = 0; i < 5; i++) { output.Clear(); Validate(runtime.Execute(program)); }
    var samples = new List<object>();
    for (int i = 0; i < 5; i++)
    {
        output.Clear();
        long allocated = GC.GetTotalAllocatedBytes(true);
        var timer = Stopwatch.StartNew();
        var value = runtime.Execute(program);
        timer.Stop();
        long bytes = GC.GetTotalAllocatedBytes(true) - allocated;
        Validate(value);
        samples.Add(new { execute_ms = timer.Elapsed.TotalMilliseconds, workload_ms = double.Parse(output[1][11..]), managed_allocated_bytes = bytes });
    }
    var counter = new Counter(new WasmtimeEngine());
    using var countedRuntime = new WasmRuntime(builtins, counter);
    output.Clear(); Validate(countedRuntime.Execute(program));
    results[name] = new {
        valid = true, samples, source_sha256 = Hash(sourcePath),
        wasm_sha256 = Convert.ToHexString(SHA256.HashData(program.Bytes.Span)).ToLowerInvariant(),
        native_calls = counter.NativeCalls, capability_lookups = counter.Lookups,
        scheduler_entries = counter.SchedulerEntries, explicit_host_collection_calls = counter.Collections,
        guest_heap_high_water_bytes = counter.Instance!.Invoke("aqua_heap_bytes"), result = output[0]
    };
    Console.WriteLine($"{name}: validated, {counter.NativeCalls} native calls, {counter.SchedulerEntries} scheduler entries");
}

// Controlled diagnostic substitutions at the engine boundary. The guest still
// performs its own allocation-pressure collections and per-block checkpoints.
var tuning = new Dictionary<string, object>();
foreach (string name in new[] { "collatz", "fibonacci", "binary_trees", "spectral_norm", "matrix", "mandelbrot" })
{
    var spec = baseline.RootElement.GetProperty("benchmarks").GetProperty(name);
    var program = new WasmCompiler().Compile(File.ReadAllText(Path.Combine(root, "benchmarks", "aquarius", name + ".aqua")));
    var modes = new List<(string Name, int Budget, bool SkipCollection)> {
        ("unchanged", 4096, false), ("budget_65536", 65536, false)
    };
    if (name == "collatz") modes.Add(("skip_host_requested_collection", 4096, true));
    var rng = new Random(20261013 + name.Length);
    modes = modes.OrderBy(_ => rng.Next()).ToList();
    foreach (var mode in modes)
    {
        var lines = new List<string>();
        var builtins = new Builtins();
        builtins.BuiltinFuncs["印出"] = new BuiltinObj(values => { lines.Add(string.Join(" ", values.Select(v => v.Inspect()))); return null!; });
        builtins.BuiltinFuncs["加入"] = BuiltinObj.FromPortable(4, _ => throw new InvalidOperationException("Host append used."));
        var engine = new TuningEngine(new WasmtimeEngine(), mode.Budget, mode.SkipCollection);
        using var runtime = new WasmRuntime(builtins, engine);
        var samples = new List<double>();
        string? failure = null;
        for (int i = 0; i < 10; i++)
        {
            lines.Clear();
            IObject value;
            try { value = runtime.Execute(program); }
            catch (InvalidOperationException caughtError) when (mode.SkipCollection) { failure = caughtError.Message; break; }
            if (value is ErrorObj error) throw new InvalidOperationException(error.Message);
            double actual = double.Parse(lines[0][7..]), expected = spec.GetProperty("expected").GetDouble();
            double tolerance = spec.TryGetProperty("relative_tolerance", out var relative) ? Math.Max(spec.GetProperty("absolute_tolerance").GetDouble(), Math.Abs(expected) * relative.GetDouble()) : 0;
            if (!double.IsFinite(actual) || Math.Abs(actual - expected) > tolerance) throw new InvalidOperationException("Incorrect tuning probe.");
            double elapsed = double.Parse(lines[1][11..]);
            if (!(elapsed > 0)) throw new InvalidOperationException("Invalid tuning clock.");
            if (i >= 5) samples.Add(elapsed);
        }
        tuning[name + "/" + mode.Name] = new { valid = failure == null, error = failure, budget = mode.Budget, skip_host_requested_collection = mode.SkipCollection, workload_ms = samples };
        Console.WriteLine($"tuning {name}/{mode.Name}: {(failure == null ? "validated" : failure)}");
    }
}

// These hand-written kernels test a possible fast path, not the Aquarius compiler.
var probes = new Dictionary<string, object>();
using (var instance = new WasmtimeEngine().Instantiate(File.ReadAllBytes(args[2]), new Dictionary<string, Delegate>()))
{
    foreach (var probe in new[] { (Name: "fibonacci", Export: "fib", N: 28, Expected: 317811), (Name: "collatz", Export: "collatz", N: 10000, Expected: 849666) })
    {
        var samples = new List<double>();
        for (int i = 0; i < 10; i++)
        {
            var timer = Stopwatch.StartNew();
            int result = instance.Invoke(probe.Export, probe.N);
            timer.Stop();
            if (result != probe.Expected) throw new InvalidOperationException("Incorrect typed probe.");
            if (i >= 5) samples.Add(timer.Elapsed.TotalMilliseconds);
        }
        probes[probe.Name] = new { n = probe.N, expected = probe.Expected, valid = true, elapsed_ms = samples };
        Console.WriteLine($"typed {probe.Name}: validated");
    }
}
var binaries = new[] { typeof(WasmRuntime).Assembly.Location, typeof(WasmtimeEngine).Assembly.Location, Path.Combine(AppContext.BaseDirectory, "Wasmtime.Dotnet.dll"), Path.Combine(AppContext.BaseDirectory, "wasmtime.dll") };
File.WriteAllText(args[3], JsonSerializer.Serialize(new {
    method = "Original standard scripts compiled once, Wasm program and session reused, five in-process warmups then five samples. Workload timer excludes source/engine compilation and output. Execute timer also includes entry, output capture and cleanup. Counters run separately in a fresh session. Managed allocation is allocation traffic; guest heap is a high-water mark. Typed probes are hand-written Wasm for bounded standard inputs, without generic semantics or scheduler safepoints.",
    baseline = Path.GetFullPath(args[1]), baseline_sha256 = Hash(args[1]),
    dotnet = System.Environment.Version.ToString(),
    process_affinity_mask = OperatingSystem.IsWindows() ? "0x" + Process.GetCurrentProcess().ProcessorAffinity.ToInt64().ToString("x") : null,
    fingerprints = binaries.ToDictionary(p => Path.GetFileName(p)!, Hash), results,
    typed_probes = probes, typed_probes_sha256 = Hash(args[2]),
    tuning_method = "Diagnostic engine wrapper changes only aqua_run budget or suppresses explicit host-to-guest aqua_collect calls. Allocation-pressure guest collection is retained. Six original numeric/array workloads; independent sessions; five warmups/five samples per mode; mode order shuffled deterministically. Not a production change or proof of host-resource/interactive correctness.",
    tuning_probes = tuning
}, new JsonSerializerOptions { WriteIndented = true }) + "\n");

sealed class Counter(IWasmEngine inner) : IWasmEngine
{
    public int NativeCalls, Lookups, SchedulerEntries, Collections;
    public IWasmInstance? Instance;
    public IWasmInstance Instantiate(ReadOnlyMemory<byte> bytes, IReadOnlyDictionary<string, Delegate> imports)
    {
        var service = (Func<int, int, int, int, int, int, int, int>)imports["service"];
        var wrapped = new Dictionary<string, Delegate> { ["service"] = (Func<int, int, int, int, int, int, int, int>)((op, context, subject, name, arguments, count, output) => {
            if (op == 1) NativeCalls++;
            if (op == 0) Lookups++;
            return service(op, context, subject, name, arguments, count, output);
        }) };
        return Instance = new Counted(inner.Instantiate(bytes, wrapped), this);
    }
    sealed class Counted(IWasmInstance instance, Counter owner) : IWasmInstance
    {
        public int Invoke(string name, params int[] arguments) {
            if (name == "aqua_run") owner.SchedulerEntries++;
            if (name == "aqua_collect") owner.Collections++;
            return instance.Invoke(name, arguments);
        }
        public Span<byte> Memory(int address, int length) => instance.Memory(address, length);
        public void Dispose() => instance.Dispose();
    }
}

sealed class TuningEngine(IWasmEngine inner, int budget, bool skipCollection) : IWasmEngine
{
    public IWasmInstance Instantiate(ReadOnlyMemory<byte> bytes, IReadOnlyDictionary<string, Delegate> imports) => new Tuned(inner.Instantiate(bytes, imports), budget, skipCollection);
    sealed class Tuned(IWasmInstance instance, int budget, bool skipCollection) : IWasmInstance
    {
        public int Invoke(string name, params int[] arguments) {
            if (name == "aqua_run") arguments[1] = budget;
            if (name == "aqua_collect" && skipCollection) return 0;
            return instance.Invoke(name, arguments);
        }
        public Span<byte> Memory(int address, int length) => instance.Memory(address, length);
        public void Dispose() => instance.Dispose();
    }
}

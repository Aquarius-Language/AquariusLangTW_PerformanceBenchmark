using System.Diagnostics;
using System.Globalization;
using System.Security.Cryptography;
using System.Text.Json;
using AquariusLang.Object;
using AquariusLang.runtime;
using AquariusLang.Wasm;
using AquariusLang.Desktop.runtime;

CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
if (args.Length != 3) throw new ArgumentException("Usage: FollowupProfile benchmark-root reference-report.json output.json");
string root = Path.GetFullPath(args[0]);
using var reference = JsonDocument.Parse(File.ReadAllText(args[1]));
var results = new Dictionary<string, object>();
string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
foreach (var item in reference.RootElement.GetProperty("benchmarks").EnumerateObject())
{
    string sourcePath = Path.Combine(root, "benchmarks", "aquarius", item.Name + ".aqua");
    var program = new WasmCompiler().Compile(File.ReadAllText(sourcePath));
    var lines = new List<string>(); var builtins = new Builtins();
    builtins.BuiltinFuncs["印出"] = new BuiltinObj(values => { lines.Add(string.Join(" ", values.Select(v => v.Inspect()))); return null!; });
    builtins.BuiltinFuncs["加入"] = BuiltinObj.FromPortable(4, _ => throw new InvalidOperationException("Host append used."));
    builtins.BuiltinFuncs["長度"] = BuiltinObj.FromPortable(1, _ => throw new InvalidOperationException("Host length used."));
    void Validate(IObject? value)
    {
        if (value is ErrorObj error) throw new InvalidOperationException(error.Message);
        if (lines.Count != 2 || !lines[0].StartsWith("RESULT ") || !lines[1].StartsWith("ELAPSED_MS ")) throw new InvalidOperationException("Invalid output.");
        double actual = double.Parse(lines[0][7..]), expected = item.Value.GetProperty("expected").GetDouble();
        double tolerance = item.Value.TryGetProperty("relative_tolerance", out var relative) ? Math.Max(item.Value.GetProperty("absolute_tolerance").GetDouble(), Math.Abs(expected) * relative.GetDouble()) : 0;
        if (!double.IsFinite(actual) || Math.Abs(actual - expected) > tolerance) throw new InvalidOperationException($"Incorrect {item.Name}: {actual}");
        double elapsed = double.Parse(lines[1][11..]);
        if (!double.IsFinite(elapsed) || elapsed <= 0) throw new InvalidOperationException("Invalid clock.");
    }
    using var runtime = new WasmRuntime(builtins, new WasmtimeEngine());
    for (int i = 0; i < 5; i++) { lines.Clear(); Validate(runtime.Execute(program)); }
    var samples = new List<object>();
    for (int i = 0; i < 7; i++)
    {
        lines.Clear(); long allocated = GC.GetTotalAllocatedBytes(true); var timer = Stopwatch.StartNew();
        var value = runtime.Execute(program); timer.Stop(); long bytes = GC.GetTotalAllocatedBytes(true) - allocated; Validate(value);
        samples.Add(new { workload_ms = double.Parse(lines[1][11..]), execute_ms = timer.Elapsed.TotalMilliseconds, managed_allocated_bytes = bytes });
    }
    var counter = new Counter(); using var counted = new WasmRuntime(builtins, counter);
    lines.Clear(); Validate(counted.Execute(program));
    int? generation = null;
    try { generation = counter.Instance!.Invoke("aqua_collection_generation"); } catch (InvalidDataException) { }
    results[item.Name] = new {
        valid = true, source_sha256 = Hash(sourcePath), wasm_sha256 = Convert.ToHexString(SHA256.HashData(program.Bytes.Span)).ToLowerInvariant(), samples,
        native_calls = counter.NativeCalls, capability_lookups = counter.Lookups, scheduler_entries = counter.SchedulerEntries,
        explicit_host_collection_calls = counter.Collections, guest_collection_generation = generation,
        budget = counter.LastBudget, guest_heap_high_water_bytes = counter.Instance!.Invoke("aqua_heap_bytes"), result = lines[0]
    };
    Console.WriteLine($"{item.Name}: validated; {counter.SchedulerEntries} scheduler entries, {counter.Collections} explicit collections");
}
var binaries = new[] { typeof(WasmRuntime).Assembly.Location, typeof(WasmtimeEngine).Assembly.Location, Path.Combine(AppContext.BaseDirectory, "Wasmtime.Dotnet.dll"), Path.Combine(AppContext.BaseDirectory, "wasmtime.dll") };
File.WriteAllText(args[2], JsonSerializer.Serialize(new {
    method = "Original standard sources; same reference checks; modules and sessions reused; five actual in-process warmups then seven measured samples. Compilation and output excluded from workload_ms. execute_ms also includes entry, captured output and cleanup. Counters measured in a separate fresh session. Guest heap is high-water, managed bytes are allocation traffic, and explicit collection counts exclude internal guest collections. Runs sequentially, no concurrent tests/benchmarks.",
    dotnet = System.Environment.Version.ToString(),
    process_affinity_mask = OperatingSystem.IsWindows() ? "0x" + Process.GetCurrentProcess().ProcessorAffinity.ToInt64().ToString("x") : null,
    fingerprints = binaries.ToDictionary(p => Path.GetFileName(p)!, Hash), results
}, new JsonSerializerOptions { WriteIndented = true }) + "\n");

sealed class Counter : IWasmEngine
{
    public int NativeCalls, Lookups, SchedulerEntries, Collections, LastBudget;
    public IWasmInstance? Instance;
    public IWasmInstance Instantiate(ReadOnlyMemory<byte> bytes, IReadOnlyDictionary<string, Delegate> imports)
    {
        var service = (Func<int, int, int, int, int, int, int, int>)imports["service"];
        var wrapped = new Dictionary<string, Delegate> { ["service"] = (Func<int, int, int, int, int, int, int, int>)((op, context, subject, name, arguments, count, output) => {
            if (op == 1) NativeCalls++; if (op == 0) Lookups++; return service(op, context, subject, name, arguments, count, output);
        }) };
        return Instance = new Counted(new WasmtimeEngine().Instantiate(bytes, wrapped), this);
    }
    sealed class Counted(IWasmInstance instance, Counter owner) : IWasmInstance
    {
        public int Invoke(string name, params int[] arguments) {
            if (name == "aqua_run") { owner.SchedulerEntries++; owner.LastBudget = arguments[1]; }
            if (name == "aqua_collect") owner.Collections++;
            return instance.Invoke(name, arguments);
        }
        public Span<byte> Memory(int address, int length) => instance.Memory(address, length);
        public void Dispose() => instance.Dispose();
    }
}

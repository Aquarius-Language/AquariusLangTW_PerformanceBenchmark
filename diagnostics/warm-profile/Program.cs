using System.Diagnostics;
using System.Globalization;
using System.Text.Json;
#if LEGACY
using AquariusLang.VM;
#else
using AquariusLang.Desktop.runtime;
using AquariusLang.Wasm;
#endif
using AquariusLang.Object;
using AquariusLang.runtime;
using AquariusLang.utils;

// Use the released compiler/runtime assemblies. Compile nothing in the language
// repository. Timing and callback instrumentation are separate passes.
if (args.Length != 2) throw new ArgumentException("Usage: WarmProfile artifact-directory output.json");
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
string directory = Path.GetFullPath(args[0]);
using var comparison = JsonDocument.Parse(File.ReadAllText(Path.Combine(directory, "comparison.json")));
var results = new Dictionary<string, object>();
foreach (var path in Directory.GetFiles(directory, "*.wasm").OrderBy(p => p)) {
    string name = Path.GetFileNameWithoutExtension(path);
#if LEGACY
    var program = new VmCompiler().Compile(File.ReadAllText(Path.ChangeExtension(path, ".aqua")));
#else
    var program = WasmProgram.Load(path);
#endif
    var spec = comparison.RootElement.GetProperty("cases").GetProperty(name + "/wasm_precompiled");
    double expected = spec.GetProperty("expected").GetDouble();
    var builtins = new Builtins();
    string? output = null;
    builtins.BuiltinFuncs["印出"] = new BuiltinObj(values => {
        output = string.Join(" ", values.Select(v => v.Inspect())); return null!;
    });
    // Same array-copy implementation as DesktopBuiltins; these workloads use no
    // other capabilities. Avoid initializing graphics for an execution profile.
    builtins.BuiltinFuncs["加入"] = new BuiltinObj(values =>
        new ArrayObj(Utils.PushToArray(((ArrayObj)values[0]).Elements, values[1])));
    builtins.BuiltinFuncs["長度"] = new BuiltinObj(values => new IntegerObj(((ArrayObj)values[0]).Elements.Length));
    void Validate(IObject? value) {
        if (value is ErrorObj error) throw new InvalidOperationException(error.Message);
        if (output == null || !output.StartsWith("RESULT ")) throw new InvalidOperationException("Missing output");
        double actual = double.Parse(output[7..], CultureInfo.InvariantCulture);
        var tolerances = spec.GetProperty("spec");
        double tolerance = tolerances.TryGetProperty("relative_tolerance", out var relative)
            ? Math.Max(tolerances.GetProperty("absolute_tolerance").GetDouble(), Math.Abs(expected) * relative.GetDouble()) : 0;
        if (!double.IsFinite(actual) || Math.Abs(actual - expected) > tolerance)
            throw new InvalidOperationException($"Incorrect {name}: {actual}, expected {expected}");
    }
#if LEGACY
    var runtime = new VirtualMachine(builtins);
#else
    var runtime = new WasmRuntime(builtins, new WasmtimeEngine());
#endif
    for (int i = 0; i < 3; i++) { output = null; Validate(runtime.Execute(program)); }
    var samples = new List<object>();
    for (int i = 0; i < 3; i++) {
        long allocated = GC.GetTotalAllocatedBytes(true);
        int[] collections = Enumerable.Range(0, 3).Select(GC.CollectionCount).ToArray();
        output = null;
        var timer = Stopwatch.StartNew();
        var value = runtime.Execute(program);
        timer.Stop();
        long allocatedBytes = GC.GetTotalAllocatedBytes(true) - allocated;
        int[] gcCollections = Enumerable.Range(0, 3).Select(g => GC.CollectionCount(g) - collections[g]).ToArray();
        Validate(value);
        samples.Add(new { elapsed_ms = timer.Elapsed.TotalMilliseconds, allocated_bytes = allocatedBytes, gc_collections = gcCollections });
    }
#if LEGACY
    results[name] = new { samples, result = output, valid = true };
    Console.WriteLine($"{name}: legacy execution profile complete");
#else
    var countedEngine = new CountingEngine(new WasmtimeEngine());
    output = null;
    Validate(new WasmRuntime(builtins, countedEngine).Execute(program));
    results[name] = new { samples, import_calls = countedEngine.Calls,
        total_import_calls = countedEngine.Calls.Values.Sum(), wasm_export_entries = countedEngine.ExportEntries,
        result = output, valid = true };
    Console.WriteLine($"{name}: {countedEngine.Calls.Values.Sum():N0} host imports, {countedEngine.ExportEntries:N0} export entries");
#endif
    File.WriteAllText(args[1], JsonSerializer.Serialize(new {
#if LEGACY
        method = "Bytecode compiled once and reused in one .NET process; 3 warmups then 3 timed executions. Minimal builtins match the Wasm profile, including exact push helper. Parsing/compilation excluded.",
#else
        method = "Same WasmProgram reused in one .NET process; 3 warmups then 3 timed executions. Each Execute still creates its own store/imports. Minimal builtins preserve print results and use the exact DesktopBuiltins push helper. Import counters run separately from timings.",
#endif
        dotnet = System.Environment.Version.ToString(), results
    }, new JsonSerializerOptions { WriteIndented = true }));
}

#if !LEGACY
sealed class CountingEngine(IWasmEngine inner) : IWasmEngine {
    public Dictionary<string, long> Calls { get; } = new();
    public long ExportEntries;
    public IWasmInstance Instantiate(ReadOnlyMemory<byte> bytes, IReadOnlyDictionary<string, Delegate> imports) {
        var wrapped = new Dictionary<string, Delegate>();
        foreach (var pair in imports) {
            string name = pair.Key;
            Calls[name] = 0;
            void Count() => Calls[name]++;
            wrapped[name] = pair.Value switch {
                Action fn => (Action)(() => { Count(); fn(); }),
                Action<int> fn => (Action<int>)(n => { Count(); fn(n); }),
                Func<int> fn => (Func<int>)(() => { Count(); return fn(); }),
                _ => throw new InvalidOperationException("Unknown signature")
            };
        }
        return new CountedInstance(inner.Instantiate(bytes, wrapped), this);
    }
    sealed class CountedInstance(IWasmInstance inner, CountingEngine owner) : IWasmInstance {
        public Func<int, int> GetFunction(int index) {
            var fn = inner.GetFunction(index);
            return pc => { owner.ExportEntries++; return fn(pc); };
        }
        public void Dispose() => inner.Dispose();
    }
}
#endif

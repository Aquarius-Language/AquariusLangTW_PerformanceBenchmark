using System.Globalization;
using System.Text.Json;
using AquariusLang.Desktop.runtime;
using AquariusLang.Object;
using AquariusLang.runtime;
using AquariusLang.utils;
using AquariusLang.Wasm;

// This pass collects counters, not timing samples. Production timings come from
// the unchanged benchmark suite and the separate interleaved comparison.
if (args.Length != 3) throw new ArgumentException("Usage: ArchitectureProfile artifact-directory original-results.json output.json");
CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
using var original = JsonDocument.Parse(File.ReadAllText(args[1]));
var rows = new Dictionary<string, object>();
foreach (string variant in new[] { "before", "after" }) {
    foreach (string path in Directory.GetFiles(Path.Combine(args[0], variant), "*.wasm").Order()) {
        string name = Path.GetFileNameWithoutExtension(path), key = name + "/" + variant;
        var program = WasmProgram.Load(path); var builtins = new Builtins(); string? output = null;
        builtins.BuiltinFuncs["印出"] = new BuiltinObj(values => {
            if (values.Length == 2 && values[0].Inspect() == "RESULT") output = values[1].Inspect();
            return null!;
        });
        builtins.BuiltinFuncs["加入"] = new BuiltinObj(values => new ArrayObj(Utils.PushToArray(((ArrayObj)values[0]).Elements, values[1])));
        builtins.BuiltinFuncs["長度"] = new BuiltinObj(values => new IntegerObj(((ArrayObj)values[0]).Elements.Length));
        var engine = new ObservedEngine(); using var runtime = new WasmRuntime(builtins, engine);
        var value = runtime.Execute(program);
        if (value is ErrorObj error) throw new InvalidOperationException(key + ": " + error.Inspect());
        double expected = original.RootElement.GetProperty("benchmarks").GetProperty(name).GetProperty("expected").GetDouble();
        var spec = original.RootElement.GetProperty("benchmarks").GetProperty(name);
        double tolerance = spec.TryGetProperty("relative_tolerance", out var relative)
            ? Math.Max(spec.GetProperty("absolute_tolerance").GetDouble(), Math.Abs(expected) * relative.GetDouble()) : 0;
        if (output == null || !double.TryParse(output, CultureInfo.InvariantCulture, out double actual) ||
            !double.IsFinite(actual) || Math.Abs(actual - expected) > tolerance)
            throw new InvalidOperationException(key + ": result validation failed: " + output);
        var counters = new Dictionary<string, int>();
        foreach (string export in new[] { "aqua_heap_bytes", "aqua_numeric_fast_calls", "aqua_numeric_fallback_calls", "aqua_numeric_depth_fallbacks" }) {
            if (export.Contains("numeric") && variant == "before") continue;
            counters[export] = engine.Instance!.Invoke(export);
        }
        rows[key] = new { result = output, valid = true, counters, run_entries = engine.Runs,
            host_imports = engine.Imports, numeric_adapters = program.Metadata.Functions.Count(f => f.NumericTable != 0) };
        Console.WriteLine(key + ": validated counters");
    }
}
File.WriteAllText(args[2], JsonSerializer.Serialize(new {
    method = "One fresh execution per preserved/new artifact on the final host. Minimal builtins preserve array-copy behavior. Counters run separately from all production timing samples; heap bytes are guest heap high-water, not cumulative allocation.",
    rows
}, new JsonSerializerOptions { WriteIndented = true }) + "\n");

sealed class ObservedEngine : IWasmEngine {
    public IWasmInstance? Instance;
    public int Runs;
    public Dictionary<string, long> Imports = new();
    public IWasmInstance Instantiate(ReadOnlyMemory<byte> bytes, IReadOnlyDictionary<string, Delegate> imports) {
        var counted = new Dictionary<string, Delegate>();
        foreach (var (name, function) in imports) {
            Imports[name] = 0;
            counted[name] = function switch {
                Action f => (Action)(() => { Imports[name]++; f(); }),
                Action<int> f => (Action<int>)(arg => { Imports[name]++; f(arg); }),
                Func<int> f => (Func<int>)(() => { Imports[name]++; return f(); }),
                Func<int, int, int, int, int, int, int, int> f => (Func<int, int, int, int, int, int, int, int>)((op, context, subject, member, arguments, count, output) => {
                    Imports[name]++; return f(op, context, subject, member, arguments, count, output);
                }),
                _ => throw new InvalidOperationException("Unexpected import signature: " + name)
            };
        }
        return Instance = new ObservedInstance(new WasmtimeEngine().Instantiate(bytes, counted), this);
    }
    sealed class ObservedInstance(IWasmInstance inner, ObservedEngine owner) : IWasmInstance {
        public int Invoke(string name, params int[] arguments) { if (name == "aqua_run") owner.Runs++; return inner.Invoke(name, arguments); }
        public Span<byte> Memory(int address, int length) => inner.Memory(address, length);
        public void Dispose() => inner.Dispose();
    }
}

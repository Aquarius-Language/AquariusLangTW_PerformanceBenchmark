# Why the WASM migration did not improve Aquarius performance

Investigation date: 2026-10-10, Asia/Taipei. The current implementation compiles
control flow to WebAssembly but leaves arithmetic, variable access, operand
stacks, arrays, closures, and function scheduling in the C# host. This retains
the expensive dynamic runtime work and adds frequent Wasm/native/managed
transitions. The measured new release is slower on every benchmark in this suite.

There is also an independent measurement problem: the published benchmark still
selects the old VM, so its latest score does not measure the migration at all.

## The published report selected the old runtime

The existing `results/latest.json`, collected at 13:20 on October 10, names:

```text
C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-014125-5fa3198b\aqua\AquariusDesktopVMREPL.exe
```

The older reports at 01:48 and 13:20 use the same executable and VM assembly
fingerprints. Their performance differences are repeat measurements of the same
runtime, not evidence about Wasm. The prior 01:29 report uses another legacy VM
release. None of the saved published runs selects the new Wasm runtime.

[run_benchmarks.py](../run_benchmarks.py) searches only for
`AquariusDesktopVMREPL.exe` / `AquariusDesktopVMREPL` at line 273 and constructs
`[executable, source.aqua]` at line 308. Runtime fingerprinting at line 85 records
only the legacy VM assemblies. The new release ships `AquariusDesktop.exe` and
`aqua.exe`, with `AquariusCore.dll` and `AquariusDesktop.dll`.

For source execution, explicitly choosing the new `AquariusDesktop.exe` works
with the existing command shape. Choosing `aqua.exe` alone does not: its commands
are `build source.aqua -o output.wasm` and `run output.wasm`.

## Direct measurements of both releases

Compared the published legacy release above with:

```text
C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-131132-54744f3e\aqua
```

The process comparison ran all ten standard workloads plus a trivial print
program, in randomized order, with one discarded process warmup and three measured
samples per mode. All **132 process executions** passed the existing reference
answer validation. Both release fingerprints, source/Wasm hashes, commands,
outputs, and individual samples are in
[comparison.json](../results/wasm-investigation/20261010/comparison.json).

Median milliseconds; smaller is faster:

| Workload | Legacy source | Wasm source | Wasm built before timing | Wasm/legacy |
| --- | ---: | ---: | ---: | ---: |
| Fibonacci(28) | 439.546 | 1022.865 | 1051.660 | 2.39× |
| Ackermann(3, 6) | 208.061 | 505.167 | 496.231 | 2.38× |
| Sieve(10000) | 161.764 | 264.318 | 265.705 | 1.64× |
| Quicksort(2000) | 157.641 | 258.534 | 254.272 | 1.61× |
| Matrix(45) | 227.527 | 392.752 | 397.364 | 1.75× |
| Mandelbrot(80) | 287.020 | 648.804 | 642.232 | 2.24× |
| N-Queens(8) | 178.489 | 334.292 | 347.308 | 1.95× |
| Binary trees(12) | 187.088 | 406.072 | 394.851 | 2.11× |
| Spectral norm(60) | 342.306 | 746.923 | 757.935 | 2.21× |
| Collatz(10000) | 611.012 | 1210.357 | 1240.815 | 2.03× |
| Trivial print | 113.194 | 184.894 | 178.990 | — |

The geometric mean of the ten Wasm/legacy ratios is **2.013× slower**. Building
Wasm first does not materially change this conclusion. Small differences between
source and prebuilt execution should not be interpreted as speedups; there are
only three measured samples and startup differs slightly between the CLIs.

To exclude process startup and reuse the compiled module, a second diagnostic
loaded the actual released assemblies into separate .NET 8.0.31 processes for
each runtime. Each workload had three in-process warmups and three timed
executions. Parsing/source compilation happened before timing. The Wasm program
object was reused, allowing the existing Wasmtime module cache to work. Each
Wasm Execute still creates and disposes its own store and host bindings.

The profiler uses matching minimal builtins: print captures the result, and array
append calls the exact `Utils.PushToArray` helper used by DesktopBuiltins. Graphics
initialization is excluded. Every output passed reference validation. Managed
allocation is total allocated bytes, **not peak memory or retained memory**.

| Workload | Warm legacy ms | Warm Wasm ms | Wasm/legacy | Legacy allocated MB | Wasm allocated MB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fibonacci | 231.943 | 652.826 | 2.81× | 662.33 | 851.59 |
| Ackermann | 88.171 | 140.620 | 1.59× | 115.08 | 155.72 |
| Sieve | 28.995 | 46.282 | 1.60× | 420.05 | 420.32 |
| Quicksort | 17.415 | 38.750 | 2.23× | 42.60 | 42.59 |
| Matrix | 60.446 | 110.386 | 1.83× | 98.95 | 99.00 |
| Mandelbrot | 117.894 | 243.482 | 2.07× | 148.52 | 148.32 |
| N-Queens | 37.368 | 83.024 | 2.22× | 38.59 | 38.42 |
| Binary trees | 43.630 | 105.004 | 2.41× | 93.32 | 120.89 |
| Spectral norm | 147.023 | 336.058 | 2.29× | 207.80 | 235.44 |
| Collatz | 406.522 | 831.383 | 2.05× | 560.79 | 560.45 |

The warmed geometric mean slowdown is **2.078×**. This rules out startup as the
sole explanation. Raw data:
[Wasm warm profile](../results/wasm-investigation/20261010/warm_profile.json),
[legacy warm profile](../results/wasm-investigation/20261010/legacy_warm_profile.json).

## The execution costs

### Arithmetic and locals do not execute as native Wasm arithmetic and locals

[WasmCompiler.cs](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:104)
emits a host import call for each value operation. For example, `n - 1` becomes
host calls to load `n`, materialize a numeric object, and subtract. It does not
become a Wasm local plus a native numeric subtraction.

The actual emitted artifacts were decoded with
[inspect_wasm.py](inspect_wasm.py). All eleven modules have zero additional Wasm
locals beyond the continuation parameter, no numeric arithmetic/comparison
instructions, no Wasm memory operations, and no direct calls to other compiled
Aquarius functions. **Every Wasm call targets one of the 45 ABI imports.** Native
Wasm instructions implement branches, continuation constants, and dispatch.
See [opcode inventory](../results/wasm-investigation/20261010/opcode_inventory.json).

[WasmRuntime.cs](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmRuntime.cs:154)
handles loads/assignments and arithmetic in C#.
[ValueOperations.cs](C:/OfficialProjects/AquariusLangTW/AquariusCore/ValueOperations.cs:19)
performs dynamic numeric checks, computes through double values, and allocates
numeric wrapper results. This runtime work is outside the Wasm compiler's
optimization scope.

### Very frequent host transitions and continuations

An instrumented engine counted each actual import invocation and exported function
entry. Counting ran in a separate execution from timing and allocation samples.

| Workload | Wasm→C# host calls | C#→Wasm export entries | Checkpoint host calls |
| --- | ---: | ---: | ---: |
| Fibonacci | 16,969,547 | 2,056,916 | 4,113,829 |
| Collatz | 26,849,348 | 1,258 | 5,149,256 |
| Spectral norm | 8,878,278 | 288,262 | 1,604,308 |
| Mandelbrot | 7,007,439 | 208 | 845,524 |

[WasmCompiler.cs:132](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:132)
ends a compiled continuation at every language call.
[WasmRuntime.cs:118](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmRuntime.cs:118)
creates an argument array, environment, and frame for script calls. The host's
scheduler enters an exported Wasm function again at
[line 195](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmRuntime.cs:195).
Deep recursion remains safe, but this is a costly convention for tiny functions.

[WasmCompiler.cs:117](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:117)
also imports `checkpoint` at every basic block. A 4,096-block quantum limits when
the scheduler resumes, but does not remove the millions of per-block checkpoint
transitions. Approximately 24% of Fibonacci's and 19% of Collatz's import calls
are checkpoints; these are call-count shares, not measured CPU-time shares.

### Allocation costs remain, and script-call allocation increased

[WasmRuntime.Frame](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmRuntime.cs:75)
owns a `List<IObject?>` and loop stack per call. Numeric literals allocate objects,
and each loop iteration constructs a fresh lexical environment with two
dictionaries. Fibonacci allocated about 852 MB and triggered 68 generation-0
collections in each timed warm sample. This is allocation traffic, not an
852 MB resident-memory claim.

The previous `VirtualMachine.cs`, read from parent commit `d1fdd2f`, used one
execution-wide operand array and bound script arguments directly from it. Its
call implementation also supported borrowed builtin arguments. The new Wasm
`Call` allocates an argument array before classifying the callee and always invokes
`builtin.Fn(args)`. Per-frame lists and argument arrays are concrete extra work.
Measured Fibonacci allocations rose from 662 MB to 852 MB, about 29%.

Collatz allocations are nearly unchanged while execution becomes 2.05× slower.
This supports transition/scheduling costs as an additional cause, rather than
attributing the entire regression to garbage collection. These measurements are
not a sampled CPU profile and do not assign an exact percentage of time to each
mechanism.

### Startup, caches, and workload construction also matter

The trivial program costs 113 ms on the old CLI and 179 ms on the prebuilt-Wasm
CLI. These tiny workloads amplify process/.NET startup and engine setup costs.
The main harness launches a fresh process for every warmup and sample, so its
warmups do not preserve JIT state.

[WasmtimeEngine.cs](C:/OfficialProjects/AquariusLangTW/AquariusDesktop/runtime/WasmtimeEngine.cs:12)
uses a default Engine and a process-local cache keyed by the byte-array identity.
Each fresh process calls `Module.FromBytes` again. Aquarius source→Wasm compilation
is distinct from Wasmtime's Wasm→machine-code compilation; an existing `.wasm`
does not remove the latter. Wasmtime documents explicit compilation caching or
machine-code precompilation for this purpose in
[its fast-compilation guide](https://docs.wasmtime.dev/examples-fast-compilation.html).

Array append still copies the whole backing array. The sieve initializes 10,001
elements with repeated append, causing quadratic copying and about 420 MB of
allocation in both runtimes. A new target cannot change that algorithmic cost.

## What to change first

1. **Make the benchmark select and identify the current backend.** Support source
   execution through `AquariusDesktop.exe` and a separate compile-before-timing
   mode through `aqua build` / `aqua run`. Record the actual core, desktop, and
   Wasmtime assemblies. Report fresh-process and warm execution separately.
2. **Put numeric loops and local values inside Wasm.** Add guarded specialization
   using Wasm numeric locals and operations, with a dynamic fallback. Preserve
   Aquarius's existing integer conversion/division/overflow behavior, eager
   evaluation, and mutable values that escape to native hosts. Merely selecting
   a more aggressive Wasmtime optimization level cannot specialize these opaque
   C# imports.
3. **Reduce import and continuation frequency.** Keep synchronous script calls and
   values within Wasm where possible, or batch operations across the ABI. Preserve
   deep-recursion and browser async behavior. Move checkpoint budget accounting
   into Wasm or amortize host polling, preserving cancellation and browser yielding.
4. **Restore efficient frame/argument storage.** Reuse execution-owned operand
   storage, bind script arguments without temporary arrays, and honor borrowed
   builtin calls where safe. Reuse loop environments only when closure capture
   semantics permit it. Avoid interning publicly mutable numeric objects.
5. **Then reduce cold startup and array-copy costs.** Evaluate Wasmtime's compiled
   module cache/precompilation and reusable host instances. Add pre-sized or
   growable array APIs and benchmark them as a distinct implementation; changing
   only one language's initialization would change the comparison.

The migration provides a portable Wasm artifact and compiled control flow. It has
not yet implemented the numeric/local-value optimizations needed for these CPU
benchmarks. Faster startup alone will not remove the warmed regression.

## Reproduction

The diagnostics leave the published README and `latest.json` untouched. Set a
fresh output directory when preserving multiple comparisons. The machine's SDK
is in the user `.dotnet` directory; the `dotnet` on PATH has only runtimes.

```powershell
$diagPython = 'C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe'
$diagDotnet = 'C:\Users\templ\.dotnet\dotnet.exe'
$diagLegacy = 'C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-014125-5fa3198b\aqua'
$diagWasm = 'C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-131132-54744f3e\aqua'
$diagOutput = 'results\wasm-investigation\rerun'

& $diagPython diagnostics\compare_wasm.py --legacy "$diagLegacy\AquariusDesktopVMREPL.exe" --wasm-cli "$diagWasm\aqua.exe" --output-dir $diagOutput --repetitions 3 --warmups 1
& $diagPython diagnostics\inspect_wasm.py $diagOutput "$diagOutput\opcode_inventory.json"

$env:DOTNET_CLI_HOME = Join-Path (Get-Location) '.benchmark-work\dotnet'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$diagWasmObj = Join-Path (Get-Location) '.benchmark-work\warm-profile-obj\'
$diagLegacyObj = Join-Path (Get-Location) '.benchmark-work\legacy-profile-obj\'
& $diagDotnet build diagnostics\warm-profile\WarmProfile.csproj -c Release --output .benchmark-work\warm-profile "-p:AquariusRelease=$diagWasm" "-p:BaseIntermediateOutputPath=$diagWasmObj" --configfile diagnostics\warm-profile\NuGet.Config
& $diagDotnet build diagnostics\warm-profile\WarmProfile.csproj -c Release --output .benchmark-work\legacy-profile -p:Legacy=true "-p:AquariusRelease=$diagLegacy" "-p:BaseIntermediateOutputPath=$diagLegacyObj" --configfile diagnostics\warm-profile\NuGet.Config
& $diagDotnet .benchmark-work\warm-profile\WarmProfile.dll $diagOutput "$diagOutput\warm_profile.json"
& $diagDotnet .benchmark-work\legacy-profile\WarmProfile.dll $diagOutput "$diagOutput\legacy_warm_profile.json"
```

Limits: these are local Windows x64 Release measurements of the specified ten
workloads, with three timed samples. CPU frequency, temperature, scheduling,
background activity, and .NET tiering were not controlled. They establish a
regression for this suite and explain plausible architectural causes; they do
not establish performance for all Aquarius programs, browsers, or platforms.
No production language implementation or main benchmark harness was modified.

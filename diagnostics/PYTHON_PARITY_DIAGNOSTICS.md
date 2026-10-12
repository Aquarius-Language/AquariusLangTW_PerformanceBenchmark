# AquariusLang performance diagnosis and path to Python parity

Investigation: October 13, 2026, Asia/Taipei.

**The tested Aquarius Wasm build needs approximately a 3.40× improvement to match
CPython 3.12.10 across this suite. The main opportunities are collection policy,
compiler-resolved variables, typed values in Wasm locals, and cheaper script calls.**
The existing Wasm backend has substantial headroom: the problem is the work emitted
around each language operation, rather than an inherent inability of Wasm to compete
with Python.

This report distinguishes measured improvements from proposed compiler work. It
adds diagnostic tools and evidence; it does not implement production optimizations.

## Evidence and scope

The fresh baseline uses the same Aquarius binaries as the October 12 published
report: `.benchmark-work/elapsed-compiler/bin/AquariusCli/release/aqua.exe`.
It covers all ten standard workloads, five measured fresh-process samples and one
discarded process warmup per language. All **180 executions** passed reference
validation. Rankings use the internal workload timers, excluding startup, initial
compilation and output.

The warm profiler uses the identical Core, Desktop and Wasmtime assemblies and
original benchmark sources. It compiles each source once and reuses its guest
session, with five actual in-process warmups and five timed samples. A separate
execution counts capability calls, scheduler entries and host-requested guest
collections. All ten workloads passed. Its API compilation uses `main.aqua` as
the module name, whereas CLI packaging uses the source filename; the whole-module
hashes are recorded separately. Source and runtime fingerprints are checked by
the analysis tool.

The sibling `C:/OfficialProjects/AquariusLangTW` source was also inspected. It has
new graphics linking, string indexing and hash mutation/transport changes beyond
the measured snapshot. The relevant name lookup, numeric emission, script-call
and collection mechanisms remain present. **These timings identify the measured
build, not a freshly rebuilt version of that sibling checkout.** See
[source fingerprints](../results/python-parity/20261013/source-fingerprints.json).

Raw evidence:

- [Fresh baseline JSON](../results/python-parity/20261013/20261013-010151-664939/results.json)
  and [generated baseline report](../results/python-parity/20261013/BASELINE.md).
- [Warm profile and controlled experiments](../results/python-parity/20261013/warm-profile.json).
- [Python construction variants](../results/python-parity/20261013/idiomatic-python.json).
- [Derived medians and ratios](../results/python-parity/20261013/analysis.json).

## How much faster Aquarius must become

Milliseconds; the ratio is Aquarius time divided by Python time. A ratio above one
means Aquarius is slower. The reduction column is the fraction of current Aquarius
workload time that must disappear to reach the measured Python median.

| Workload | Aquarius ms | Python ms | Ratio | Required time reduction |
| --- | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 201.488 | 26.442 | 7.62× | 86.9% |
| Ackermann | 41.864 | 11.440 | 3.66× | 72.7% |
| Sieve | 13.356 | 37.590 | 0.36× | Already ahead for this implementation |
| Quicksort | 11.533 | 4.477 | 2.58× | 61.2% |
| Matrix multiplication | 74.727 | 12.635 | 5.91× | 83.1% |
| Mandelbrot | 34.643 | 20.256 | 1.71× | 41.5% |
| N-Queens | 15.789 | 3.656 | 4.32× | 76.8% |
| Binary trees | 74.215 | 8.405 | 8.83× | 88.7% |
| Spectral norm | 128.368 | 14.481 | 8.86× | 88.7% |
| Collatz | 194.552 | 83.408 | 2.33× | 57.1% |

The equally weighted geometric mean slowdown is **3.395×**. A uniform improvement
of that size means reducing elapsed time by **70.5%**. Optimizing just binary trees,
spectral norm and Fibonacci to Python parity would still leave the whole suite
approximately **1.79× slower**. Several shared runtime costs must improve.

The target here is ordinary CPython running explicit algorithms. Matching Python
with NumPy, native numerical libraries or alternative Python runtimes is a separate
goal requiring corresponding library benchmarks and implementations.

## First measurable improvement: collect less often without breaking ownership

`WasmHostRuntime.Session.Run` requests `Collect()` whenever the guest yields its
4,096-basic-block budget. `Collect()` calls the guest's full `aqua_collect`, then
uses its native liveness results to release host handles. The guest also has its
own collection trigger at 8 MiB of allocation pressure.

| Workload | Scheduler entries | Explicit host-requested collections | Guest heap high-water bytes |
| --- | ---: | ---: | ---: |
| Fibonacci | 1,005 | 1,004 | 21,536 |
| Binary trees | 129 | 128 | 1,188,816 |
| Spectral norm | 392 | 391 | 20,272 |
| Collatz | 1,258 | 1,257 | 2,032 |

Heap high-water marks are not allocation traffic, live memory or process peak
memory. Even a small heap can receive substantial allocation/reuse traffic.
These counters also exclude collections invoked internally by the guest.

A controlled engine wrapper changed only the `aqua_run` budget to 65,536, retaining
guest checkpoints and collection logic. Each mode used its own session, five
warmups and five samples. Mode order was shuffled. All **120 executions** across
the six workloads and two modes passed validation.

| Workload | Budget 4,096 ms | Budget 65,536 ms | Measured speedup |
| --- | ---: | ---: | ---: |
| Binary trees | 76.171 | 31.099 | **2.45×** |
| Spectral norm | 125.955 | 69.612 | **1.81×** |
| Fibonacci | 188.851 | 146.417 | 1.29× |
| Mandelbrot | 34.316 | 28.020 | 1.22× |
| Collatz | 188.357 | 160.558 | 1.17× |
| Matrix | 70.746 | 61.563 | 1.15× |

This experiment changes scheduler return frequency and its associated collections
together; it does not isolate their individual CPU shares. It demonstrates a
useful optimization direction, but still leaves large gaps against Python.

An additional negative control suppressed explicit host-to-guest collection calls
for Collatz. It failed with `Invalid native service request`: the host consumed
stale native-liveness information and released a still-needed capability.
**Blindly skipping collection is incorrect.** No timings from that failed control
are used as performance evidence.

Recommended implementation:

1. Separate cancellation/yield decisions from collection decisions. Trigger guest
   collection by allocation pressure, pending ownership work or a bounded periodic
   policy, rather than automatically at every scheduler return.
2. Give liveness results an explicit collection generation. Reclaim native handles
   only using fresh results from a completed trace.
3. Iterate occupied builtin/native roots instead of scanning all 65,536 builtin
   scope slots and clearing the entire native-liveness table each time. Preserve
   correctness for recycled IDs and callback reentry.
4. Allow a larger desktop batch budget while preserving a short browser budget.
   Retain independent cancellation checks; benchmark latency and interactive
   responsiveness before choosing defaults.

Evidence locations in the measured snapshot:
[host scheduling](../.benchmark-work/elapsed-source/AquariusCore/wasm/WasmHostRuntime.cs#L214),
[guest collection](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L224),
[guest checkpoint](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L176).
The corresponding current source is in the sibling language repository.

## Largest compiler opportunity: resolved bindings and typed data flow

The compiler lowers identifiers into name-based `Load` instructions. The runtime
looks up bindings through scope chains, using string comparison or scope indexes.
Loop-containing functions have guarded binding caches, but the shared `scope_epoch`
invalidates these caches when scopes change, including every loop iteration.
Functions without loops do not get that cache allocation. A cache is also different
from a binding resolved to a stable local slot at compile time.

Add a binding-resolution pass that classifies parameters, local variables,
captured cells, module globals and unresolved dynamic names. Assign stable slots
to ordinary locals and parameters. Keep captured variables in shared cells, and
retain guarded dynamic lookup where module projection, reentry or changing scope
structure requires it. Avoid global invalidation for unrelated scopes.

Then add a typed, control-flow-aware IR with liveness information. Keep stable
numeric values in Wasm `i32`, `f32` or `f64` locals across expressions and loop
iterations. Spill values to the tagged runtime representation at suspension,
capture and capability boundaries where necessary. Add constant propagation,
dead temporary elimination, common expression reuse and safe loop-invariant
hoisting. Resolve `benchmark_n` once when it cannot change during a kernel.

The emitter already has native numeric instructions, but those operations load
two **16-byte tagged values** from the guest operand stack, check their tags,
compute a result, convert it according to Aquarius rules, and store another tagged
value. Its six scratch Wasm locals do not hold source variables throughout a
function. Loads, array indexing, increment and compound assignment still go through
guest runtime helpers. For example, `total += coefficient * src[j]` still involves
generic array access, memory-stack traffic and compound-assignment handling.

CPython's own specialization work targets variables, operations and calls with
guards and fallbacks; this is relevant design precedent, not a predicted Aquarius
speedup. See [PEP 659](https://peps.python.org/pep-0659/).

Evidence: [identifier lowering](../.benchmark-work/elapsed-source/AquariusCore/LoweringCompiler.cs#L88),
[numeric emission](../.benchmark-work/elapsed-source/AquariusCore/wasm/WasmCompiler.cs#L121),
[binding cache](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L150),
[iteration invalidation](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L218).

## Tiny functions need a cheaper call path

Every language call ends the emitted continuation. A script call creates a guest
scope, binds parameters by name and allocates a guest frame. The guest scheduler
dispatches the callee through its Wasm function table and later resumes the caller.
This supports deep recursion and suspension, but imposes substantial fixed work
on tiny functions such as `fib`, `element`, tree construction and tree traversal.

Priorities:

- Inline small, statically known, nonrecursive functions when their binding and
  side-effect behavior permit it. Spectral norm's `element` is an obvious candidate;
  protect against rebinding of that function's global name.
- Add a guarded direct-call path for synchronous, known callees with stable types.
  Keep the existing resumable path for suspension, reentry and uncertain callees.
- Reuse stack/arena frame storage and bind argument slots directly. Allocate
  captured environments only when escape analysis requires them.
- Perform tail-call elimination where valid. Naive Fibonacci is not tail-recursive,
  so this feature alone cannot fix its benchmark.
- Use direct structured loops/branches in synchronous optimized regions, while
  retaining continuation dispatch at actual suspension boundaries.

A direct recursive fast path needs a depth guard or another way to preserve deep
recursion behavior. Functions cannot lose cancellation, errors or browser yielding
just because their arguments are numeric.

Evidence: [call emission](../.benchmark-work/elapsed-source/AquariusCore/wasm/WasmCompiler.cs#L169),
[frame construction](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L142),
[script call](../.benchmark-work/elapsed-source/AquariusCore/wasm/runtime/runtime.c#L195).

### Feasibility experiment: the backend can run the algorithms much faster

Two hand-written Wasm kernels use typed locals and arithmetic, direct Fibonacci
recursion, and ordinary nested Collatz loops. They retain the benchmark algorithms:
no memoization, cached answers or replacement formulas. Compilation is excluded;
each probe has five warmups and five timed invocations, and all outputs match.

| Kernel | Generic Aquarius warm ms | Hand-written typed Wasm ms | CPython baseline ms |
| --- | ---: | ---: | ---: |
| Fibonacci(28) | 189.899 | **1.463** | 26.442 |
| Collatz(10000) | 189.751 | **1.220** | 83.408 |

These are **feasibility measurements, not implemented Aquarius speedups**. The
probes omit generic types, binding lookup, the scheduler, collection and
cancellation. They are valid only for the tested bounded arithmetic: Fibonacci's
result is 317,811, and Collatz's largest intermediate is 27,114,424, both within
signed 32-bit range. They show that a typed fast path can provide enough headroom
to exceed the measured Python speed, without establishing that a general compiler
will reproduce these numbers.

## Useful performance features

| Feature | Why it helps | First workloads to validate |
| --- | --- | --- |
| Pre-sized arrays and fill constructors | Avoid per-element language calls and temporary array headers during initialization | Sieve, matrix, spectral norm |
| Explicit mutable growable vectors with reserve | Provide amortized append without changing snapshot-style `push` semantics | Quicksort, data ingestion |
| Typed contiguous arrays/buffers | Store numbers directly, specialize indexing and reduce tag/memory overhead | Matrix, spectral norm, image/pixel loops |
| Fixed-layout records | Give fields fixed offsets and allow selective tracing of reference fields | Binary trees, application objects |
| Bulk numerical operations | Amortize language dispatch and enable blocking/vectorization inside Wasm libraries | Matrix and vector workloads |
| Optional type annotations/contracts | Help prove specialization where inference cannot; define their semantics explicitly | Numeric APIs and kernels |
| Indexed collection hashes | Replace linear pair searches with collision-safe indexes for larger hashes | New hash-heavy tests; absent from this suite |
| Compiler/profiler diagnostics | Explain selected fast paths, fallback reasons, allocation, collection and call costs | Every benchmark |

Names in this table describe proposed capabilities, not existing syntax/API promises.
Automatic inference should make common code faster without requiring annotations.
Typed buffers also need bulk ownership/transport contracts if they cross graphics,
audio or other capability boundaries.

The runtime already shares array storage for compatible appends and detaches on
writes. Recommending copy-on-write as a new feature would repeat completed work.
A mutable vector API can still avoid allocating a distinct header on every append;
fixed-size construction can avoid append calls altogether.

SIMD, matrix blocking, worker threads and GPU kernels are later extensions. They
help appropriate bulk workloads, but do not remove small-call or ordinary scalar
loop overhead. Keep numerical-library comparisons separate from the scalar suite.

## Correct the interpretation of the Python comparison

The suite intentionally uses Python `list + [item]` during initialization. The
current Aquarius runtime can share backing storage, whereas Python concatenation
copies the list. Both preserve independent array/list snapshots, but their physical
allocation costs differ. The generated README's statement that Aquarius `push`
always copies the full array is stale for this build.

Separate Python-only variants preserve the algorithms and checksums but use
preallocation for the sieve and ordinary `.append()` for quicksort/matrix setup.
Each variant has one fresh-process warmup and five randomized samples. All
**36 executions** passed validation.

| Workload | Python copy/append ms | Python idiomatic setup ms | Setup-variant speedup |
| --- | ---: | ---: | ---: |
| Sieve | 35.505 | **1.115** | 31.85× |
| Quicksort | 4.001 | **1.408** | 2.84× |
| Matrix | 11.993 | **8.514** | 1.41× |

Aquarius's original sieve time is about **12×** the separately measured idiomatic
Python sieve. The published sieve win is legitimate for those selected scripts,
but does not show that Aquarius has faster ordinary sieve execution than Python.
These variant results are not substituted into the official composite score.

Maintain two labeled suites: equivalent operations/snapshot semantics, and
idiomatic implementations using each language's normal collection APIs. Add
allocation-free scalar loops, tiny calls, local versus captured/global lookup,
preallocated array reads/writes and captured versus uncaptured loop scopes as
microbenchmarks. Separate initialization, computation, collection and transport
when attributing causes.

## Implementation order and acceptance gates

| Order | Deliverable | Evidence/gate |
| --- | --- | --- |
| 1 | Collection policy, liveness-generation contract and desktop/browser budget controls | Reproduce the measured gains; preserve cancellation latency, native-resource lifetime and reentry |
| 2 | Compiler-resolved local/parameter slots and capture analysis | Lookup microbenchmarks improve; shadowing, rebinding and closure tests remain correct |
| 3 | Typed data flow, Wasm locals, specialized compound assignment/indexing | Matrix, Mandelbrot and Collatz improve without changing numeric behavior |
| 4 | Inlining, guarded direct calls and cheaper fallback frames | Fibonacci, Ackermann, spectral norm and trees improve; deep recursion and async cases pass |
| 5 | Pre-sized/typed collections, records and bulk library operations | Idiomatic comparisons and larger workloads improve; alias/ownership behavior passes |

For suite parity, require a geometric mean Aquarius/Python time ratio at or below
1.0, and report every per-workload ratio so a regression cannot hide in the mean.
For a stronger claim of matching Python on every tested workload, require each
ratio at or below 1.0. Use repeated runs and uncertainty estimates before declaring
close results decisive.

Preserve these behaviors in all optimized paths:

- Aquarius integer division truncates; integer arithmetic uses its documented
  conversion rules, including `INT_MIN` for out-of-range/nonfinite results. Plain
  wrapping `i32` arithmetic is not generally equivalent. Float rounding, numeric
  promotion and left-type-preserving compound assignment also matter.
- Boolean operators are eager. Exceptions/errors and side effects retain their
  order. Globals, builtin shadowing and function rebinding remain observable.
- Loop-body declarations have per-iteration scope; escaping closures retain their
  own iteration bindings. Mutable aliases and appended-array snapshots remain valid.
- Array reads outside bounds return null; writes outside bounds produce a language
  error. Bounds-check elimination needs a proof or guard.
- Captured references and suspended arguments stay rooted across collection;
  callbacks, disposal, native handles and browser suspension remain correct.

Caching and lazy graphics initialization already exist. Startup/AOT launcher work
can improve launch latency, but the published workload timer excludes startup and
initial compilation. It cannot by itself remove this 3.40× computational gap.
Wasmtime documents [compilation caching/precompilation](https://docs.wasmtime.dev/examples-fast-compilation.html)
and [guest/native profiling approaches](https://docs.wasmtime.dev/examples-profiling.html).
Use a sampled guest CPU profile to allocate effort within the remaining runtime
helpers; the counters here are call counts, not exact CPU-time attribution.

## Reproduction

Run from the benchmark repository. The profiler currently targets Windows x64.

```powershell
$parityPython = 'C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe'
$parityDotnet = 'C:\Users\templ\.dotnet\dotnet.exe'
$parityRelease = Join-Path (Get-Location) '.benchmark-work\elapsed-compiler\bin\AquariusCli\release'
$parityOutput = 'results\python-parity\rerun'

& $parityPython run_benchmarks.py --aquarius "$parityRelease\aqua.exe" --repetitions 5 --warmups 1 --output-dir $parityOutput --readme "$parityOutput\BASELINE.md"
& $parityPython diagnostics\python-parity-profile\idiomatic_python_probe.py "$parityOutput\idiomatic-python.json"
& $parityPython diagnostics\python-parity-profile\make_typed_probes.py "$parityOutput\typed-probes.wasm"

$env:DOTNET_CLI_HOME = Join-Path (Get-Location) '.benchmark-work\dotnet'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$parityObj = Join-Path (Get-Location) '.benchmark-work\parity-profile-obj\'
& $parityDotnet build diagnostics\python-parity-profile\ParityProfile.csproj -c Release --output .benchmark-work\parity-profile "-p:AquariusRelease=$parityRelease" "-p:BaseIntermediateOutputPath=$parityObj" --configfile diagnostics\warm-profile\NuGet.Config
& $parityDotnet .benchmark-work\parity-profile\ParityProfile.dll . "$parityOutput\latest.json" "$parityOutput\typed-probes.wasm" "$parityOutput\warm-profile.json"
& $parityPython diagnostics\python-parity-profile\analyze.py $parityOutput
```

The deliberately disabled-collection control is expected to fail and is recorded
as invalid while other experiments continue. It illustrates an ownership dependency.
The report, tools and raw output remain separate from the published README/results.

Limitations: local Windows 11 x64, Intel i9-13900H, Balanced power plan, affinity
mask `0xfffff`, five timed samples. CPU frequency, thermal state, background work
and scheduling are uncontrolled. Tuning modes are shuffled groups rather than
interleaved individual executions. Native typed probes deliberately omit general
language guarantees. No sampled CPU attribution or retained/process-peak memory
measurement was collected. Browser and other platforms need independent validation.

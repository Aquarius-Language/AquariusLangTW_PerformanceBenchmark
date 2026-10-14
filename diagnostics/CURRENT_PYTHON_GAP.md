# Why AquariusLang still trails Python

Investigation: October 14, 2026, Asia/Taipei. Measurements use the published
`AquariusCompiler-win-x64-20261014-164034-81083bd1` release and CPython 3.12.10.

Aquarius already beats Python on Collatz. It has not surpassed Python across this
suite because small function calls, lexical bindings and generic value handling
still require substantial runtime work inside Wasm. The remaining problem is the
compiler/runtime execution model, rather than an inherent limit of WebAssembly.

The published suite puts Aquarius **1.273× slower overall**. A new comparison
that replaces Python's repeated list concatenation with ordinary construction in
all five affected scripts puts Aquarius **2.045× slower overall**. The latter is
a separately labeled experiment; the published results are preserved.

## Current performance, with Python's list construction corrected

Seven measured fresh-process samples and one discarded process warmup per case;
all cases shuffled each round. The timers include initialization and computation,
and exclude startup, source/Wasm compilation and printing. Algorithms and reference
answers are retained; no NumPy, native algorithm library or memoization is used.
Aquarius uses the repository's current array APIs.

| Workload | Aquarius ms | Python ms | Aquarius/Python time |
| --- | ---: | ---: | ---: |
| Fibonacci | 103.676 | 25.459 | 4.07× |
| Ackermann | 19.199 | 10.857 | 1.77× |
| Sieve | 1.921 | 1.086 | 1.77× |
| Quicksort | 4.839 | 1.512 | 3.20× |
| Matrix | 12.794 | 9.293 | 1.38× |
| Mandelbrot | 27.927 | 20.265 | 1.38× |
| N-Queens | 10.039 | 3.505 | 2.86× |
| Binary trees | 20.738 | 7.843 | 2.64× |
| Spectral norm | 40.512 | 14.663 | 2.76× |
| Collatz | 63.540 | 80.415 | 0.79× |

The ratio is the equal-weight geometric mean across ten workloads, not the ratio
of total milliseconds. Uniform time reductions to parity would be **21.5%** for
the published comparison or **51.1%** for the construction-corrected comparison.
These aggregate targets do not guarantee parity on each workload.

## 1. Script calls still allocate scopes and frames and return through a scheduler

The emitter terminates the current continuation at every script call. The guest
runtime resolves the closure, allocates a scope, declares parameters by name,
allocates a frame, dispatches through its function table, and eventually resumes
the caller. Functions do not receive an ordinary typed Wasm argument/return ABI.

This fixed work is expensive for tiny functions. Naive Fibonacci(28) executes
1,028,457 function invocations, derived from its recursion tree. Spectral norm
calls the small `element(i, j)` function **144,000 times**. Both need little useful
work per call, making the generic call convention a strong explanation for their
remaining losses.

A controlled source probe manually inlined `element` while retaining the same
matrix formula, loops and checksum:

| Run | Original ms | Inlined ms | Speedup |
| --- | ---: | ---: | ---: |
| Initial probe | 38.254 | 25.781 | 1.48× |
| Complete comparison | 40.512 | 25.241 | 1.60× |

The complete probe removes **37.7% of elapsed time**, but the inlined program is
still about **1.72× slower** than Python's 14.663 ms. This is evidence for optimizing
tiny calls and their associated binding work. It does not isolate call CPU time:
inlining changes binding locality, declarations and continuation structure too.

Frame capacity is at least 16 tagged operands, even for small functions. The
allocator rounds blocks to powers of two and initializes each frame header.
Free lists already reuse memory, but allocation, initialization, parameter binding
and cleanup still occur on each invocation.

Evidence: [call emission](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:248),
[guest script call](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:242),
[frame allocation](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:151),
[scheduler](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:177),
[operand capacity](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmStackAnalysis.cs:84).

## 2. Binding optimization stops at the current lexical scope

Candidate slots are computed only for the current scope, using `scopes.Peek()`.
Entering a loop pushes a new scope. Consequently, a function parameter or enclosing
loop variable accessed inside a nested loop usually falls back to name resolution,
even when it is an ordinary local that never escapes.

For example, the inner matrix loop reads `a`, `b`, `i`, `j`, `benchmark_n` and
updates `total` from outer scopes. Spectral norm has the same pattern for `src`,
`transpose`, `i`, `total` and its helper function. A current-scope access also checks
binding count and name before reading its value; it is not an unboxed Wasm local.

Fallback lookup walks lexical scopes and uses linear or indexed name searches.
The shared `scope_epoch` invalidates all guarded binding caches when declarations
or loop scopes change. Every `rt_nextIteration` invalidates it and resets the loop
scope; parameter declarations in callees also invalidate it. This limits cache
reuse in precisely the loops and tiny-call workloads that dominate the suite.
Uncaptured iteration scopes are already reused, so "allocate a new scope on every
iteration" would be an outdated diagnosis.

Evidence: [slot resolution](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmBindingSlots.cs:31),
[guarded loads](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:146),
[lookup and invalidation](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:94),
[binding cache](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:159),
[loop reset](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:260).

## 3. Native arithmetic still operates on generic values in linear memory

Aquarius now emits native Wasm arithmetic, comparisons, compound assignment,
increment and guarded array reads. The old claim that every arithmetic operation
crosses into C# no longer describes this release.

However, each value remains a **16-byte `{tag, ref, double number}`** record.
The emitter copies operands onto a frame's memory stack, loads their tags and
numbers, checks numeric types, performs arithmetic, applies Aquarius's conversion
rules and writes the tagged result back. Integer operations commonly use floating
point arithmetic followed by range/conversion handling. The Wasm locals are a fixed
set of scratch temporaries, rather than persistent typed source variables.

This leaves repeated checks, stack-pointer updates, memory traffic and conversion
work across expressions and iterations. Array elements also contain tagged values;
writes use generic runtime helpers for bounds, aliasing, copy-on-write and native
dirty-buffer handling. There is no compiler pass here that carries stable numeric
types through whole loops and retains their source variables in Wasm locals.

These are concrete emitted mechanisms, not sampled CPU percentages. Their exact
contribution would need separately guarded compiler variants or guest profiling.

Evidence: [value layout](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:6),
[numeric emission](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:190),
[scratch locals](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:213),
[array writes](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:252).

## 4. Guest allocation, collection and per-block scheduling checks remain

Fresh instrumentation using the exact published Core, Desktop and Wasmtime
binaries confirms that the main work runs inside Wasm:

| Workload | Native host calls | Scheduler entries | Host-requested traces | Total guest trace generation | Guest heap high-water bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fibonacci | 4 | 63 | 1 | 83 | 21,536 |
| Binary trees | 4 | 8 | 1 | 12 | 2,107,984 |
| Spectral norm | 4 | 25 | 1 | 12 | 9,616 |
| Collatz | 4 | 79 | 1 | 1 | 2,032 |

The four native calls are the two timers and two prints; capability lookups are
counted separately. Host-requested completion collection is largely outside the
workload timer. The guest still collects at 8 MiB of allocation pressure, including
allocations satisfied from recycled blocks, and performs a full mark/sweep trace.
Fibonacci's small heap therefore does not imply little allocation activity.
Generation 83 includes the final trace and demonstrates substantial allocation
pressure despite a roughly 21 KiB heap high-water mark.

Every emitted basic block still calls the guest checkpoint helper. Loop entry,
iteration reset and exit still perform runtime work. These are guest function calls,
not millions of Wasm-to-C# transitions. Collection and checkpoint costs are plausible
remaining contributors, but this run does not assign them an exclusive CPU share.

Evidence: [allocation accounting](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:65),
[checkpoint emission](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/WasmCompiler.cs:222),
[guest checkpoint](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:186),
[collector](C:/OfficialProjects/AquariusLangTW/AquariusCore/wasm/runtime/runtime.c:266).

## Python's baseline and benchmark interpretation

CPython 3.12 benefits from the adaptive specialization, cached globals/indexing and
cheaper Python call/frame handling introduced in 3.11. A dynamic language compiled
to Wasm can still lose if it performs more administrative work per operation.
See [Python's runtime changes](https://docs.python.org/3.12/whatsnew/3.11.html#faster-runtime)
and [PEP 659](https://peps.python.org/pep-0659/). This is design context, not an
attribution of Aquarius's measured slowdown to a specific Python optimization.

The official Python scripts repeatedly use `list + [item]`. Current Aquarius
scripts use pre-sized arrays and mutable append APIs, so their setup operations no
longer have corresponding copying costs. Replacing Python construction alone gives:

| Python workload | Original ms | Ordinary construction ms | Speedup |
| --- | ---: | ---: | ---: |
| Sieve | 36.818 | 1.086 | 33.89× |
| Quicksort | 4.297 | 1.512 | 2.84× |
| Matrix | 12.587 | 9.293 | 1.35× |

N-Queens and spectral norm were also changed to preallocated Python lists in the
complete comparison. The pronounced published sieve win is mostly a construction
comparison: with ordinary setup Python takes 1.086 ms versus Aquarius's 1.921 ms.
The algorithms remain equivalent, but this is a distinct suite, not a replacement
for its historical score.

There are also language-semantic differences. Aquarius evaluates both operands of
`&&`/`||`; Python short-circuits. An N-Queens probe replaced the side-effect-free
three-way OR with explicit early exits. It measured **10.201 ms versus 10.039 ms**
original, with overlapping sample ranges. It demonstrated no speedup, so eager
boolean evaluation is **not established as a primary cause** of the N-Queens gap.
Additional branches/checkpoints may offset avoided expression work; that is an
inference, not a measured CPU breakdown.

## What to implement next

1. Add guarded inlining for tiny known callees and a cheaper synchronous call ABI.
   Reuse execution-owned frame/argument storage; retain the resumable path for
   suspension, uncertain callees and deep recursion. Validate Fibonacci, Ackermann,
   spectral norm and trees first.
2. Resolve parameters and locals across lexical loop scopes. Distinguish ordinary
   local slots from captured cells and globals; narrow invalidation to affected
   bindings. Preserve shadowing, closures, callback mutation and rebinding.
3. Add typed data flow and persistent Wasm numeric locals, with guarded fallback.
   Specialize indexing and writes for proven array ownership and bounds. Preserve
   integer conversion, floating-point rounding and observable error order.
4. Reduce scope/frame allocation accounting and tracing work using ownership and
   escape information, and amortize guest checkpoint work while preserving
   cancellation and browser responsiveness.

Collection scheduling, current-scope fast paths, copy-on-write storage and the
bulk array API are already implemented. The array-library report shows large
isolated operation gains, but only a 1.078× whole-suite gain from adopting the API.
The remaining recursive/compute kernels need compiler/runtime changes. Startup
caching cannot explain or remove the reported gap because startup and initial
compilation are excluded from these timers.

## Evidence, validation and limits

- [Published baseline](../results/20261014-164708-330679/results.json).
- [Complete variant measurements](../results/current-diagnosis/20261014/variant-probes-complete.json):
  **200 executions passed** independent result checks, including warmups.
- [Current runtime counters](../results/current-diagnosis/20261014/warm-profile.json):
  **130 executions passed**, with counters recorded in separate executions.
- [Derived ratios and fingerprints](../results/current-diagnosis/20261014/analysis.json).
- [Initial probe](../results/current-diagnosis/20261014/variant-probes.json) and its
  [preserved harness](../results/current-diagnosis/20261014/measurement_harness_initial.py):
  **192 executions passed**. It corrected Python construction in three scripts.
- [Complete measured harness](../results/current-diagnosis/20261014/measurement_harness.py)
  and [reusable diagnostic](diagnose_current.py).
- [Existing fast paths](C:/OfficialProjects/AquariusLangTW/docs/performance-fast-paths.md)
  and [array-library measurements](../results/array-library/20261014/README.md).

Core, Desktop and both Wasmtime binary hashes match the published baseline, and
the warm profiler's source hashes match all ten published Aquarius sources.
Inspected sibling-source hashes are recorded separately; no claim is made that
the current checkout's Git state was verified against the release commit.

The API profiler's warmed timings were variable and substantially slower than the
fresh CLI samples despite identical binaries. Its timings are preserved but used
only as diagnostic data; they are not used for ranking or a claimed warm/cold
speedup. The deterministic counters and the separately shuffled CLI experiments
support the findings above. No sampled CPU profile was collected, so mechanisms
other than the source substitutions have not been assigned exact time shares.

These results describe this Windows x64 machine and these ten scripts. CPU
frequency, background load, scheduling and temperature were not controlled.
Heap high-water values are not allocation traffic or peak process memory.
The production compiler/runtime and the published benchmark sources were not edited.

The subsequent [performance architecture proposal](PERFORMANCE_ARCHITECTURE.md)
develops a larger compiler/execution redesign for drastic improvements.

Reproduce the complete CLI experiment into a new output file:

```powershell
& C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe diagnostics\diagnose_current.py `
  --aquarius C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261014-164034-81083bd1\aqua\aqua.exe `
  --output results\current-diagnosis\repeat.json --repetitions 7
```

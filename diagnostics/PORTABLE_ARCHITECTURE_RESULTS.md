# Portable architecture performance diagnosis

October 15, 2026, Asia/Taipei. Final code and rebuilt release; unchanged algorithms.

Aquarius is **1.76× faster than its original release** across the ten
workloads in the interleaved comparison, reducing aggregate geometric-mean workload
time by **43.0%**. Fibonacci improves
**14.8×**, matrix multiplication
**2.1×**, and Mandelbrot
**2.0×**. Every new median is at least as fast in this paired run;
Ackermann is essentially unchanged, and the small tree difference is not a large gain.

On the existing matched-semantics suite Aquarius now has **1.39× Python's
geometric-mean speed**. Against the separate idiomatic Python variants, Aquarius
still takes **1.154× as long overall** (15.4% slower).
The implementation improves the architecture substantially; it does not establish
universal superiority over Python or optimized native libraries.

## What changed

The implemented portable portion of the [architecture proposal](PERFORMANCE_ARCHITECTURE.md)
selects an execution representation according to the function's proven behavior:

- Closed, effect-free scalar functions use resolved Wasm locals, structured control
  flow and private typed calling conventions. A successful call needs no guest
  lexical scope or language frame. Mixed numeric helpers retain tag/payload registers.
- A control-flow/type proof gives integer-only functions untagged `i32` locals and
  direct integer recursive calls. Checked `i64` arithmetic preserves Aquarius overflow
  conversion; division guards zero and minimum-integer divided by minus one.
- Recursive target identity, argument type/payload, initialization, fuel and depth
  guards retain the generic path when assumptions fail. Failed pure speculation
  restores its original budget before generic execution, preserving call state at
  an observable yield. Deep recursion disables repeated speculative entry.
- The compiler resolves candidate bindings through enclosing lexical scopes.
  Capture, count and name guards retain dynamic lookup after host insertion,
  closure mutation, conditional declarations or shadowing.

These are shared compiler/Wasm changes. No operating-system-specific fast path,
CPU-specific backend, engine tuning, algorithm rewrite, Boolean short-circuit
change or floating-point reassociation is introduced. General arrays still hold
tagged elements. Full SSA, typed array storage, capture cells and materialized
optimized continuations remain future architectural work.

See the language's [implementation notes](C:/OfficialProjects/AquariusLangTW/docs/portable-numeric-architecture.md).
The external capability ABI remains version 2. New artifacts use 32-byte function
definitions and require the rebuilt hosts. Current hosts retain compatibility with
older ABI 2 artifacts that use the original 24-byte layout.

## Old versus new under the same conditions

Each benchmark uses one warmup and nine measured repetitions for four variants:
preserved Aquarius, new Aquarius, CPython and Node. Their execution order is shuffled
each round. Aquarius programs are compiled before timing; the workload timer includes
initialization and computation, and excludes process startup, initial compilation
and output. This is not a startup-performance measurement. Source hashes, inputs,
checksums and tolerances match across old/new cases.

| Workload | Original median ms | New median ms | Original / new speed |
| --- | ---: | ---: | ---: |
| Recursive Fibonacci | 107.783 | 7.292 | 14.78× |
| Ackermann | 19.923 | 19.894 | 1.00× |
| Sieve of Eratosthenes | 1.902 | 1.571 | 1.21× |
| Quicksort | 4.869 | 3.274 | 1.49× |
| Matrix multiplication | 13.740 | 6.507 | 2.11× |
| Mandelbrot | 29.414 | 14.602 | 2.01× |
| N-Queens | 9.718 | 8.046 | 1.21× |
| Binary trees | 21.748 | 20.728 | 1.05× |
| Spectral norm | 38.602 | 22.622 | 1.71× |
| Collatz | 64.549 | 56.947 | 1.13× |

The normal published suite independently shows **1.77×** improvement
against the preserved published medians. The original publication used five measured
repetitions; the new publication uses nine. The interleaved result above is preferred
for attributing gains because it measures both releases in the same run.
All **300** normal-suite executions and **400** paired executions
passed their reference checks. Environment details and executable/Core/engine
fingerprints are retained in the raw JSON reports.

## Why the improvements differ

Counter collection runs separately from timing. It executes both old and new
artifacts on the final host, checks their results, and observes guest exports.
Fast-call counts include successful adapter entries; internal direct recursive
calls are not counted individually. Run entries are scheduler invocations, not
instruction counts or CPU-time shares.

| Workload | Scheduler entries old → new | Successful scalar entries | Failed attempts | Depth failures |
| --- | ---: | ---: | ---: | ---: |
| fibonacci | 63 → 55 | 725 | 740 | 0 |
| ackermann | 15 → 15 | 0 | 1 | 1 |
| spectral_norm | 25 → 23 | 144,000 | 0 | 0 |
| matrix | 5 → 5 | 0 | 0 | 0 |
| binary_trees | 8 → 8 | 0 | 0 | 0 |

Fibonacci benefits from avoiding repeated tag checks, numeric normalization,
scope allocation and frame dispatch inside integer recursion. Fuel guards still
require some resumable execution; the new path does not skip scheduler checks.
Ackermann reaches the direct-call depth limit once and then stays stackless, so
it retains nearly all of its original costs. Spectral norm's scalar coefficient
helper uses the typed adapter 144,000 times, with no failed attempts in this profile.

Matrix and Mandelbrot have zero scalar adapter entries. Their substantial gains
come from resolved ancestor bindings in nested loops. Quicksort, N-Queens and
Collatz also retain generic functions/loops and receive smaller binding gains.
Binary trees allocate arrays and return heap objects, so their recursive functions
are ineligible for scalar execution. The guest heap high-water remains approximately
2.11 MB; these measurements do not show allocation-churn elimination for tree code.

An initial tag/payload recursive implementation regressed Fibonacci from about
104 ms to 251 ms in the paired trial. That trial is preserved. The final implementation
adds proven integer representation and keeps recursive noninteger arguments on the
resumable path. The final paired Fibonacci result is 7.292 ms.

## The remaining Python gap

The existing Python suite deliberately mirrors Aquarius's copy-and-append setup.
The additional diagnostic replaces those Python constructions with `append` or
preallocation in five workloads, retaining algorithm inputs and reference results.
It also retains separate inlining/predicate experiments; those modified Aquarius
variants are not included in the production score or old/new improvement claim.

| Workload | New Aquarius ms | Idiomatic Python ms | Aquarius / Python time |
| --- | ---: | ---: | ---: |
| Recursive Fibonacci | 7.139 | 26.243 | 0.27× |
| Ackermann | 19.953 | 11.229 | 1.78× |
| Sieve of Eratosthenes | 1.535 | 1.204 | 1.27× |
| Quicksort | 3.286 | 1.523 | 2.16× |
| Matrix multiplication | 6.718 | 9.543 | 0.70× |
| Mandelbrot | 14.413 | 20.341 | 0.71× |
| N-Queens | 8.472 | 3.606 | 2.35× |
| Binary trees | 21.486 | 8.030 | 2.68× |
| Spectral norm | 21.290 | 14.348 | 1.48× |
| Collatz | 55.530 | 82.244 | 0.68× |

Lower ratios are better. The remaining overall ratio is **1.154×**.
The strongest next portable steps are:

1. Materialize optimized continuations at fuel/depth boundaries, allowing deep
   recursive functions such as Ackermann to keep typed values across resumptions.
   Increasing depth or changing the scheduling contract would not solve that safely.
2. Introduce homogeneous array backing storage with mutation/alias guards, and
   avoid physical copy-and-append when ownership proves the old contents cannot be
   observed. Keep the public copy/alias behavior unchanged.
3. Extend resolved values and type/effect analysis through loop regions and known
   callees, so N-Queens predicates, Quicksort and spectral loops stop paying generic
   operand-stack and binding costs for their stable scalar state.
4. Apply escape analysis/scalar replacement to temporary tree objects, followed
   by allocator work for objects that still escape. Changing the tree benchmark's
   algorithm would not be a language-runtime improvement.

These explain the measured gaps; they are not claimed as implemented speedups.
Idiomatic diagnostics validated **250** executions, and the separate
counter pass validated **20** executions.

## Correctness and build verification

| Suite | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: |
| Complete language suite (all native/graphics flags enabled; serialized collections) | 1,627 | 0 | 0 |
| Browser/WebAssembly suite | 309 | 0 | 0 |
| Language server suite | 18 | 0 | 0 |
| Final application host and scalar subset (additional rerun) | 52 | 0 | 0 |
| Benchmark harness with real compiler integration | 15 | 0 | 0 |

Differential tests compare optimized and generic execution over 1,452 mixed-type
operator pairs and 324 integer boundary pairs, plus return/type/error behavior,
overflow, nonfinite values, division, compound assignment, eager Boolean evaluation,
duplicate parameters, conditional locals, captured scope mutation, self-rebinding,
deep recursion and a recursive-binding mutation during a yield. Browser tests
exercise the same artifact on JavaScript WebAssembly, including integer arithmetic,
depth/fuel fallback and old metadata compatibility. This is broad regression evidence,
not a formal proof for every possible program.

The pinned Zig 0.15.1 source/binary check passed. The compiler and existing application
host were rebuilt from the changed source, and the 52-test packaged/scalar subset
was rerun with the final runtime pack. The first parallel native run encountered a
window-creation race; the final full run serialized collections and passed every test.
One added counter assertion was corrected to account for accumulation between executions.
No production window behavior or scheduling limit was changed to make tests pass.

## Preserved evidence and reproduction

- [Original performance backup](../results/architecture-improvement/20261015/before/README.md),
  [original raw results](../results/architecture-improvement/20261015/before/latest.json),
  and [backup fingerprints](../results/architecture-improvement/20261015/before/backup-manifest.json).
- [Published new report](../README.md),
  [new raw results](../results/architecture-improvement/20261015/after-final/latest.json),
  [paired results](../results/architecture-improvement/20261015/paired.json),
  [paired CSV](../results/architecture-improvement/20261015/paired.csv),
  and [idiomatic Python diagnosis](../results/architecture-improvement/20261015/idiomatic-python.json).
- [Counter profile](../results/architecture-improvement/20261015/counters.json),
  [initial regression trial](../results/architecture-improvement/20261015/paired-initial.json),
  [source before/after fingerprints](../results/architecture-improvement/20261015/source-changes.json),
  and [test evidence](../results/architecture-improvement/20261015/tests/all-tests.trx).
- [Machine-readable diagnosis](../results/architecture-improvement/20261015/diagnosis.json).

Final compiler: [aqua.exe](C:/OfficialProjects/AquariusLangTW/dist/releases/AquariusCompiler-win-x64-20261015-portable-architecture-final/aqua/aqua.exe).
Original release and original edited source files remain preserved. The large old
application host backup remains on disk under `source-before/runtime-pack/host.exe`
and is excluded from Git tracking.

Regenerate and revalidate this diagnosis with:

```powershell
python diagnostics/analyze_portable_architecture.py
```

Repeat the same old/new experiment using the recorded executable paths and
`diagnostics/compare_performance.py --before ORIGINAL --after FINAL --output NEW_JSON --repetitions 9`.
The counter profiler source is in `diagnostics/architecture-profile`; build it with
the final release directory as the `AquariusRelease` MSBuild property, then run it
with before/after artifact folders, original results JSON and an output JSON path.

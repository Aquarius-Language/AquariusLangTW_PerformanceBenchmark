# AquariusLang vs. Python vs. Node.js

A desktop execution benchmark with ten classic algorithms, 30 standalone source scripts, and a Python runner that validates results and generates this README plus JSON/CSV reports.

## Run it

Requirements: Python 3.10+, Node.js, and the AquariusLang desktop VM (`AquariusDesktopVMREPL`, including its bundled dependencies). No Python packages or npm install required. The Aquarius scripts use AquariusLangTW keywords and bilingual built-ins; older English-only interpreters are not compatible.

```powershell
python run_benchmarks.py
# Fast correctness check with smaller inputs:
python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0
# Override runtime discovery when necessary:
python run_benchmarks.py --aquarius "C:\Aquarius\AquariusDesktopVMREPL.exe" --node "C:\Program Files\nodejs\node.exe"
# Limit the workload selection:
python run_benchmarks.py --benchmarks fibonacci sieve matrix
# Rebuild README from an existing report without running benchmarks:
python run_benchmarks.py --report-only results/latest.json
# Harness and reference checks:
python -m unittest discover -s tests -v
```

If `python` is an unconfigured pyenv shim, invoke an installed `python.exe` directly. The runner uses its own interpreter for the Python benchmarks by default. Use `--python PATH` to override it. It searches the process PATH and, on Windows, current user/system PATH entries, so a newly added Aquarius PATH works even in an older terminal session. Runtime overrides accept one executable path, not shell command strings.

The runner stages source copies in a temporary directory and replaces only each script's `benchmark_n` declaration with its selected manifest size. Original scripts run directly with the standard sizes. Outputs go into a dated `results/` directory; `results/latest.json` and `README.md` are regenerated after each run. Use `--output-dir`, `--readme`, `--timeout`, `--seed`, `--repetitions`, and `--warmups` to customize a run. Exit code 1 means at least one runtime was unavailable or a case failed validation; failures remain visible in reports.

## Measurement method

- Each sample launches a fresh process; Python measures elapsed wall time with `perf_counter_ns` around process launch through exit and captured output. Source loading, parsing/compilation, runtime startup, allocation, garbage collection, algorithm execution, and output are included.
- Aquarius executes `.aqua` source on its desktop VM. Python uses CPython source execution; Node.js uses V8 source execution. No precompiled bottles, NumPy, native algorithm libraries, worker threads, or built-in sort are used in timed workloads.
- Discarded warmup processes prime OS file caches; they do **not** preserve a JIT or VM across measured processes. Each round shuffles all benchmark/language cases with a recorded seed and runs them sequentially.
- Every warmup and measured sample must match an untimed Python correctness oracle. Integers match exactly; spectral norm squared uses relative tolerance 1e-9 and absolute tolerance 1e-12. Nonzero exits, timeouts, missing/extra output, nonfinite results, and checksum mismatches fail the case.
- Aquarius integer `/` truncates; matching Python `//` and Node.js `Math.trunc` implement that arithmetic. Floating workloads use doubles (`d` literals in Aquarius). Standard inputs keep integer intermediates within signed 32-bit range.
- Aquarius `push`/`加入` copies the array. Python and Node.js deliberately use copy-and-append during corresponding array construction. Thus sieve, sorting, and matrix setup include quadratic copying; these are matched baseline implementations, not idiomatic peak-performance versions of each language.
- Medians describe these scripts on this machine. Small workloads can be dominated by startup; results do not isolate steady-state algorithm speed or establish a universal language ranking. CPU frequency, thermal state, background work, and scheduler noise are uncontrolled. Memory use and CPU time are not measured; RAM below describes the machine.

## Latest run

- Started: 2026-10-10T01:29:10.915910+08:00
- Finished: 2026-10-10T01:29:13.976773+08:00
- Timezone: Asia/Taipei
- Profile: `smoke`; 1 measured samples and 0 discarded warmups per case
- Order seed: 20261010; per-process timeout: 120 seconds
- OS: Windows-11-10.0.26200-SP0
- Architecture: AMD64
- CPU: 13th Gen Intel(R) Core(TM) i9-13900H; logical CPUs: 20
- Installed RAM: 31.71 GiB
- Active power plan: Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced)
- Python orchestrator: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- Timer resolution: 1e-07 seconds

| Runtime | Version / build | Executable |
| --- | --- | --- |
| AquariusLang | No version flag; see binary fingerprint and release directory | C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-003556-3f551a82\aqua\AquariusDesktopVMREPL.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.EXE |

Aquarius release directory: `C:\OfficialProjects\AquariusLangTW\dist\releases\AquariusCompiler-win-x64-20261010-003556-3f551a82\aqua`.

Aquarius apphost SHA-256: `3d18c10c9b681d6297671b81abaa3f5944de631c272a8b2d532afe1fad42fb7b`.
- `AquariusLangVM.dll` SHA-256: `779f1f8b4e008fe5947f17684e2f12e3b4a9433e61ad11b70774363d4999c8b2`
- `AquariusDesktopVMREPL.dll` SHA-256: `0375b3a4b50d8a017ff23db9893e3ddc3155f4323f4477a603c395eba03c3c05`

## Results

All durations are milliseconds. Lower is faster. Ratios are median runtime / median Python runtime; values below 1 mean faster than Python for this workload.

| Algorithm | n | Aquarius median | Python median | Node.js median | Aquarius / Python | Node.js / Python |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 12 | 120.150 | 30.377 | 41.943 | 3.96x | 1.38x |
| Ackermann | 3 | 130.402 | 33.237 | 44.314 | 3.92x | 1.33x |
| Sieve of Eratosthenes | 100 | 127.984 | 37.562 | 49.623 | 3.41x | 1.32x |
| Quicksort | 50 | 137.666 | 31.645 | 42.866 | 4.35x | 1.35x |
| Matrix multiplication | 5 | 124.357 | 38.687 | 48.046 | 3.21x | 1.24x |
| Mandelbrot | 8 | 143.141 | 39.800 | 42.071 | 3.60x | 1.06x |
| N-Queens | 5 | 140.608 | 34.103 | 44.730 | 4.12x | 1.31x |
| Binary trees | 5 | 129.305 | 35.163 | 42.387 | 3.68x | 1.21x |
| Spectral norm | 8 | 139.920 | 30.175 | 43.524 | 4.64x | 1.44x |
| Collatz | 100 | 135.405 | 29.118 | 60.812 | 4.65x | 2.09x |

### Timing variability

CV is sample standard deviation / mean. With one sample, variability cannot be estimated and is shown as a dash.

| Algorithm | Runtime | Min ms | Max ms | Std. dev. ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| fibonacci | AquariusLang | 120.150 | 120.150 | — | — | 1/1 |
| fibonacci | Python | 30.377 | 30.377 | — | — | 1/1 |
| fibonacci | Node.js | 41.943 | 41.943 | — | — | 1/1 |
| ackermann | AquariusLang | 130.402 | 130.402 | — | — | 1/1 |
| ackermann | Python | 33.237 | 33.237 | — | — | 1/1 |
| ackermann | Node.js | 44.314 | 44.314 | — | — | 1/1 |
| sieve | AquariusLang | 127.984 | 127.984 | — | — | 1/1 |
| sieve | Python | 37.562 | 37.562 | — | — | 1/1 |
| sieve | Node.js | 49.623 | 49.623 | — | — | 1/1 |
| quicksort | AquariusLang | 137.666 | 137.666 | — | — | 1/1 |
| quicksort | Python | 31.645 | 31.645 | — | — | 1/1 |
| quicksort | Node.js | 42.866 | 42.866 | — | — | 1/1 |
| matrix | AquariusLang | 124.357 | 124.357 | — | — | 1/1 |
| matrix | Python | 38.687 | 38.687 | — | — | 1/1 |
| matrix | Node.js | 48.046 | 48.046 | — | — | 1/1 |
| mandelbrot | AquariusLang | 143.141 | 143.141 | — | — | 1/1 |
| mandelbrot | Python | 39.800 | 39.800 | — | — | 1/1 |
| mandelbrot | Node.js | 42.071 | 42.071 | — | — | 1/1 |
| nqueens | AquariusLang | 140.608 | 140.608 | — | — | 1/1 |
| nqueens | Python | 34.103 | 34.103 | — | — | 1/1 |
| nqueens | Node.js | 44.730 | 44.730 | — | — | 1/1 |
| binary_trees | AquariusLang | 129.305 | 129.305 | — | — | 1/1 |
| binary_trees | Python | 35.163 | 35.163 | — | — | 1/1 |
| binary_trees | Node.js | 42.387 | 42.387 | — | — | 1/1 |
| spectral_norm | AquariusLang | 139.920 | 139.920 | — | — | 1/1 |
| spectral_norm | Python | 30.175 | 30.175 | — | — | 1/1 |
| spectral_norm | Node.js | 43.524 | 43.524 | — | — | 1/1 |
| collatz | AquariusLang | 135.405 | 135.405 | — | — | 1/1 |
| collatz | Python | 29.118 | 29.118 | — | — | 1/1 |
| collatz | Node.js | 60.812 | 60.812 | — | — | 1/1 |

## Validation

All runtime outputs matched the correctness oracles for every warmup and measured sample.

| Algorithm | Expected result | Workload |
| --- | ---: | --- |
| Recursive Fibonacci | 144 | Naive recursive Fibonacci; no memoization. |
| Ackermann | 61 | Recursive A(3, n), stressing nested function calls. |
| Sieve of Eratosthenes | 25 | Count primes up to and including n using a boolean sieve. |
| Quicksort | 464184 | In-place middle-pivot quicksort of a deterministic LCG sequence; validate order and a weighted checksum. |
| Matrix multiplication | 790 | Flat row-major matrices; explicit i/j/k cubic multiplication and sum of all result entries. |
| Mandelbrot | 1462 | n by n grid on [-2, 1) by [-1, 1), capped at 60 iterations; sum escape iteration counts. |
| N-Queens | 10 | Backtracking with explicit column and diagonal checks; count all solutions. |
| Binary trees | 504 | Build and recursively count eight complete binary trees of depth n. |
| Spectral norm | 1.6130176190135865 | Ten power iterations of the implicit benchmark matrix; return squared spectral norm to avoid a library square root. |
| Collatz | 3142 | Sum steps to reach 1 for starting integers 1 through n; no memoization. |

## Reproducibility artifacts

- Raw samples, output, commands, execution order, metadata, executable hashes, and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\results.json`
- Summary statistics and raw samples as CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\summary.csv` and `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\smoke\20261010-012910-915910\samples.csv`
- `benchmarks.json`: standard/smoke input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/python/`, `benchmarks/node/`: standalone scripts.
- `reference.py`: untimed correctness oracles; `tests/`: harness/reference regression checks.

This README is generated by `run_benchmarks.py`; edits will be overwritten on the next run. The JSON preserves hashes of both original and staged scripts and the manifest, runner, and oracle. Temporary command paths identify the files used during the run; they are removed afterward. Keep the source and its matching report together when comparing runs.

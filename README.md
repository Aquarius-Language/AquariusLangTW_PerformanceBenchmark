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

- Started: 2026-10-10T01:29:24.197590+08:00
- Finished: 2026-10-10T01:29:52.260541+08:00
- Timezone: Asia/Taipei
- Profile: `standard`; 5 measured samples and 1 discarded warmups per case
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
| Recursive Fibonacci | 28 | 494.980 | 62.716 | 58.370 | 7.89x | 0.93x |
| Ackermann | 6 | 236.301 | 46.169 | 49.566 | 5.12x | 1.07x |
| Sieve of Eratosthenes | 10000 | 187.411 | 69.709 | 85.806 | 2.69x | 1.23x |
| Quicksort | 2000 | 173.464 | 44.836 | 51.555 | 3.87x | 1.15x |
| Matrix multiplication | 45 | 241.511 | 46.959 | 59.634 | 5.14x | 1.27x |
| Mandelbrot | 80 | 322.500 | 52.631 | 57.045 | 6.13x | 1.08x |
| N-Queens | 8 | 201.441 | 36.492 | 50.908 | 5.52x | 1.40x |
| Binary trees | 12 | 215.510 | 41.617 | 56.180 | 5.18x | 1.35x |
| Spectral norm | 60 | 371.631 | 53.247 | 58.877 | 6.98x | 1.11x |
| Collatz | 10000 | 604.473 | 117.897 | 62.549 | 5.13x | 0.53x |

### Timing variability

CV is sample standard deviation / mean. With one sample, variability cannot be estimated and is shown as a dash.

| Algorithm | Runtime | Min ms | Max ms | Std. dev. ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| fibonacci | AquariusLang | 473.937 | 523.442 | 20.164 | 4.1% | 5/5 |
| fibonacci | Python | 61.448 | 88.768 | 11.997 | 17.0% | 5/5 |
| fibonacci | Node.js | 48.801 | 79.738 | 11.890 | 19.2% | 5/5 |
| ackermann | AquariusLang | 224.401 | 254.514 | 11.810 | 5.0% | 5/5 |
| ackermann | Python | 37.847 | 55.552 | 7.351 | 16.2% | 5/5 |
| ackermann | Node.js | 45.880 | 64.267 | 9.083 | 16.7% | 5/5 |
| sieve | AquariusLang | 178.776 | 227.438 | 19.104 | 9.8% | 5/5 |
| sieve | Python | 61.884 | 91.263 | 11.369 | 15.4% | 5/5 |
| sieve | Node.js | 76.808 | 92.642 | 6.331 | 7.4% | 5/5 |
| quicksort | AquariusLang | 162.598 | 191.065 | 11.027 | 6.3% | 5/5 |
| quicksort | Python | 36.002 | 68.858 | 13.114 | 27.2% | 5/5 |
| quicksort | Node.js | 45.726 | 66.806 | 9.197 | 16.5% | 5/5 |
| matrix | AquariusLang | 225.796 | 355.468 | 53.328 | 20.4% | 5/5 |
| matrix | Python | 42.143 | 53.278 | 4.272 | 9.1% | 5/5 |
| matrix | Node.js | 55.442 | 100.264 | 18.804 | 28.0% | 5/5 |
| mandelbrot | AquariusLang | 311.536 | 343.757 | 12.595 | 3.9% | 5/5 |
| mandelbrot | Python | 45.923 | 58.386 | 4.697 | 9.0% | 5/5 |
| mandelbrot | Node.js | 43.693 | 69.617 | 11.403 | 20.3% | 5/5 |
| nqueens | AquariusLang | 195.777 | 212.562 | 6.563 | 3.2% | 5/5 |
| nqueens | Python | 35.817 | 59.622 | 10.324 | 24.1% | 5/5 |
| nqueens | Node.js | 43.241 | 55.875 | 5.756 | 11.7% | 5/5 |
| binary_trees | AquariusLang | 211.042 | 326.745 | 49.466 | 20.4% | 5/5 |
| binary_trees | Python | 35.847 | 46.414 | 4.853 | 11.8% | 5/5 |
| binary_trees | Node.js | 51.423 | 152.737 | 43.306 | 54.5% | 5/5 |
| spectral_norm | AquariusLang | 355.627 | 389.834 | 12.541 | 3.4% | 5/5 |
| spectral_norm | Python | 41.781 | 57.794 | 6.002 | 11.6% | 5/5 |
| spectral_norm | Node.js | 48.402 | 107.093 | 23.496 | 35.4% | 5/5 |
| collatz | AquariusLang | 577.675 | 651.531 | 27.144 | 4.5% | 5/5 |
| collatz | Python | 109.843 | 133.637 | 10.250 | 8.6% | 5/5 |
| collatz | Node.js | 49.153 | 77.008 | 9.976 | 16.0% | 5/5 |

## Validation

All runtime outputs matched the correctness oracles for every warmup and measured sample.

| Algorithm | Expected result | Workload |
| --- | ---: | --- |
| Recursive Fibonacci | 317811 | Naive recursive Fibonacci; no memoization. |
| Ackermann | 509 | Recursive A(3, n), stressing nested function calls. |
| Sieve of Eratosthenes | 1229 | Count primes up to and including n using a boolean sieve. |
| Quicksort | 616973 | In-place middle-pivot quicksort of a deterministic LCG sequence; validate order and a weighted checksum. |
| Matrix multiplication | 545940 | Flat row-major matrices; explicit i/j/k cubic multiplication and sum of all result entries. |
| Mandelbrot | 129059 | n by n grid on [-2, 1) by [-1, 1), capped at 60 iterations; sum escape iteration counts. |
| N-Queens | 92 | Backtracking with explicit column and diagonal checks; count all solutions. |
| Binary trees | 65528 | Build and recursively count eight complete binary trees of depth n. |
| Spectral norm | 1.6236011690579917 | Ten power iterations of the implicit benchmark matrix; return squared spectral norm to avoid a library square root. |
| Collatz | 849666 | Sum steps to reach 1 for starting integers 1 through n; no memoization. |

## Reproducibility artifacts

- Raw samples, output, commands, execution order, metadata, executable hashes, and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261010-012924-197590\results.json`
- Summary statistics and raw samples as CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261010-012924-197590\summary.csv` and `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261010-012924-197590\samples.csv`
- `benchmarks.json`: standard/smoke input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/python/`, `benchmarks/node/`: standalone scripts.
- `reference.py`: untimed correctness oracles; `tests/`: harness/reference regression checks.

This README is generated by `run_benchmarks.py`; edits will be overwritten on the next run. The JSON preserves hashes of both original and staged scripts and the manifest, runner, and oracle. Temporary command paths identify the files used during the run; they are removed afterward. Keep the source and its matching report together when comparing runs.

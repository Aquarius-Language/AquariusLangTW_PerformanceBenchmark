# 陣列效能診斷 / Array performance diagnosis

Precompile each case; one untimed process warmup then seven shuffled rounds by default. Workload timers include initialization/computation and exclude process startup, compilation and printing. Each sample uses a fresh process/engine; warmup does not reuse the Wasm engine. Original/new-api scripts have identical algorithms and validated results. Microbenchmarks replace only the measured array operation.

Measurements: medians in milliseconds. Speedup = before / after; < 1 means slower.

| Case | Original runtime | New core, original script | New core + Chinese API | Core speedup | Total speedup |
| --- | ---: | ---: | ---: | ---: | ---: |
| fibonacci | 104.3864 | 105.1507 | 104.4773 | 0.993x | 0.999x |
| ackermann | 18.9478 | 19.4209 | 19.1910 | 0.976x | 0.987x |
| sieve | 3.5986 | 3.6498 | 1.9012 | 0.986x | 1.893x |
| quicksort | 4.9341 | 4.9543 | 5.0430 | 0.996x | 0.978x |
| matrix | 13.1442 | 13.1714 | 12.8535 | 0.998x | 1.023x |
| mandelbrot | 28.0954 | 27.4283 | 27.4714 | 1.024x | 1.023x |
| nqueens | 9.5325 | 9.3935 | 9.4671 | 1.015x | 1.007x |
| binary_trees | 21.3727 | 20.9506 | 20.4790 | 1.020x | 1.044x |
| spectral_norm | 37.8148 | 37.8675 | 38.6037 | 0.999x | 0.980x |
| collatz | 63.9941 | 62.4931 | 59.4107 | 1.024x | 1.077x |
| array_make | 36.5841 | 36.5409 | 2.4343 | 1.001x | 15.029x |
| array_append | 36.6810 | 36.1258 | 20.8591 | 1.015x | 1.759x |
| array_copy | 373.3920 | 375.6160 | 2.3188 | 0.994x | 161.028x |
| array_fill | 346.6305 | 346.9315 | 2.8183 | 0.999x | 122.993x |

All 10 suite cases geometric speedup: 1.078x.
Five array workloads: 1.133x.
Four isolated array operations: 26.897x.
Core changes alone, all 10 unchanged scripts: 1.003x.

Each result was checked against the existing independent reference or a fixed exact microbenchmark checksum. Full samples, spread, execution order and binary/source hashes are in comparison.json. Small changes can be timing noise; initialization is a small fraction of matrix/spectral/nqueens, so their whole-workload gain can be small. These measurements are from this desktop; portable implementation is verified separately on JavaScript WebAssembly. Array Copy/Fill/Make replace per-element Aquarius loops with core Wasm operations; Append retains the original loop and avoids persistent array headers. Quicksort still uses the original middle-pivot quicksort.

The core-only result is approximately flat. The clear gains come from adopting the array API. Quicksort and spectral_norm final medians were 2.2% and 2.1% slower; their changes are small relative to measured variation. Initialization is a small fraction of their workload.

Validation: 1,523 C# tests passed (32 existing conditional skips); 148 JavaScript WebAssembly/array regressions and 18 language-server tests passed. Core Wasm reproduced exactly with Zig 0.15.1. Both language examples compiled and ran; the Chinese example exported as a website. The rebuilt standalone host passed Chinese import, mutation and portable function projection. Android adapter registration is covered; physical Android/Linux/macOS devices were not benchmarked.

Exact measured harness: measurement_harness.py (SHA-256 is in comparison.json). The before runtime is the core source as it stood at the start of this task, freshly published in Release, not a historical report measured on another day.

Reproduce from the benchmark repository (adapt executable paths for your platform):

```powershell
python diagnostics/diagnose_arrays.py --benchmark-root . --before ../AquariusLangTW/.array-build/before/aqua.exe --after ../AquariusLangTW/.array-build/after/aqua.exe --original-scripts results/array-library/20261014/staged/before --output results/array-library/repeat --repetitions 7
```

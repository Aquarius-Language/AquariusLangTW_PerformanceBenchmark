# Desktop performance benchmark: AquariusLang, AquariusLang (typed), AquariusLang (Native AOT compiler), AquariusLang (typed, Native AOT compiler), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: Node.js 100.00, C# 61.84, AquariusLang (Native AOT compiler) 14.18, AquariusLang 14.17, AquariusLang (typed) 12.78, AquariusLang (typed, Native AOT compiler) 12.67, Python 10.84
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: Node.js 100.00, C# 51.23, AquariusLang 11.06, AquariusLang (Native AOT compiler) 10.95, AquariusLang (typed, Native AOT compiler) 9.90, AquariusLang (typed) 9.64, Python 7.81

The project provides ten classic algorithms, 112 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: Node.js 100.00, C# 61.84, AquariusLang (Native AOT compiler) 14.18, AquariusLang 14.17, AquariusLang (typed) 12.78, AquariusLang (typed, Native AOT compiler) 12.67, Python 10.84 (higher is faster).**

Pairwise composite speed: Node.js is 1.62× as fast as C#; Node.js is 7.05× as fast as AquariusLang (Native AOT compiler); Node.js is 7.06× as fast as AquariusLang; Node.js is 7.82× as fast as AquariusLang (typed); Node.js is 7.89× as fast as AquariusLang (typed, Native AOT compiler); Node.js is 9.23× as fast as Python; C# is 4.36× as fast as AquariusLang (Native AOT compiler); C# is 4.37× as fast as AquariusLang; C# is 4.84× as fast as AquariusLang (typed); C# is 4.88× as fast as AquariusLang (typed, Native AOT compiler); C# is 5.71× as fast as Python; AquariusLang (Native AOT compiler) is 1.00× as fast as AquariusLang; AquariusLang (Native AOT compiler) is 1.11× as fast as AquariusLang (typed); AquariusLang (Native AOT compiler) is 1.12× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (Native AOT compiler) is 1.31× as fast as Python; AquariusLang is 1.11× as fast as AquariusLang (typed); AquariusLang is 1.12× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang is 1.31× as fast as Python; AquariusLang (typed) is 1.01× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (typed) is 1.18× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.17× as fast as Python.

| Rank | Language | Composite score | Speed vs Node.js | Speed vs C# | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang | Speed vs AquariusLang (typed) | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Node.js | 100.00 | 1.000× | 1.617× | 7.054× | 7.058× | 7.824× | 7.893× | 9.227× |
| 2 | C# | 61.84 | 0.618× | 1.000× | 4.362× | 4.365× | 4.839× | 4.881× | 5.706× |
| 3 | AquariusLang (Native AOT compiler) | 14.18 | 0.142× | 0.229× | 1.000× | 1.001× | 1.109× | 1.119× | 1.308× |
| 4 | AquariusLang | 14.17 | 0.142× | 0.229× | 0.999× | 1.000× | 1.108× | 1.118× | 1.307× |
| 5 | AquariusLang (typed) | 12.78 | 0.128× | 0.207× | 0.902× | 0.902× | 1.000× | 1.009× | 1.179× |
| 6 | AquariusLang (typed, Native AOT compiler) | 12.67 | 0.127× | 0.205× | 0.894× | 0.894× | 0.991× | 1.000× | 1.169× |
| 7 | Python | 10.84 | 0.108× | 0.175× | 0.765× | 0.765× | 0.848× | 0.855× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| String building | 20000 | 73.313 | 72.706 | 70.915 | 72.304 | 12.109 | 0.553 | 72.212 | 6.05× | 6.00× | 5.86× | 5.97× | 0.05× | 5.96× |
| String-key hash | 500000 | 36.432 | 34.361 | 35.108 | 37.299 | 33.754 | 10.583 | 12.001 | 1.08× | 1.02× | 1.04× | 1.11× | 0.31× | 0.36× |
| Integer-key hash | 1000000 | 105.789 | 115.486 | 103.064 | 105.536 | 107.624 | 35.162 | 11.368 | 0.98× | 1.07× | 0.96× | 0.98× | 0.33× | 0.11× |
| Closures | 1000000 | 96.874 | 126.185 | 103.037 | 121.070 | 122.446 | 14.918 | 11.800 | 0.79× | 1.03× | 0.84× | 0.99× | 0.12× | 0.10× |
| Struct updates | 1000000 | 68.429 | 101.345 | 72.924 | 103.873 | 117.498 | 4.562 | 3.075 | 0.58× | 0.86× | 0.62× | 0.88× | 0.04× | 0.03× |
| Function calls | 2000000 | 8.905 | 8.387 | 8.618 | 9.109 | 131.484 | 9.629 | 6.743 | 0.07× | 0.06× | 0.07× | 0.07× | 0.07× | 0.05× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| String building | 20000 | 72.706 | 0.553 | 0.01× | Node.js, 131.45× faster |
| String-key hash | 500000 | 34.361 | 10.583 | 0.31× | Node.js, 3.25× faster |
| Integer-key hash | 1000000 | 115.486 | 35.162 | 0.30× | Node.js, 3.28× faster |
| Closures | 1000000 | 126.185 | 14.918 | 0.12× | Node.js, 8.46× faster |
| Struct updates | 1000000 | 101.345 | 4.562 | 0.05× | Node.js, 22.21× faster |
| Function calls | 2000000 | 8.387 | 9.629 | 1.15× | AquariusLang (typed), 1.15× faster |
| **Geometric mean** | | | | **0.13×** | Node.js, 7.82× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| String building | AquariusLang | 67.385 | 86.513 | 7.146 | 9.6% | 5/5 |
| String building | AquariusLang (typed) | 68.719 | 79.493 | 4.023 | 5.5% | 5/5 |
| String building | AquariusLang (Native AOT compiler) | 60.845 | 73.084 | 5.265 | 7.7% | 5/5 |
| String building | AquariusLang (typed, Native AOT compiler) | 66.058 | 75.748 | 3.946 | 5.6% | 5/5 |
| String building | Python | 11.867 | 13.609 | 0.821 | 6.5% | 5/5 |
| String building | Node.js | 0.505 | 0.629 | 0.055 | 9.8% | 5/5 |
| String building | C# | 66.102 | 94.285 | 11.848 | 15.6% | 5/5 |
| String-key hash | AquariusLang | 34.753 | 37.758 | 1.234 | 3.4% | 5/5 |
| String-key hash | AquariusLang (typed) | 33.559 | 39.511 | 2.455 | 6.9% | 5/5 |
| String-key hash | AquariusLang (Native AOT compiler) | 33.893 | 41.486 | 3.124 | 8.5% | 5/5 |
| String-key hash | AquariusLang (typed, Native AOT compiler) | 34.120 | 39.815 | 2.426 | 6.6% | 5/5 |
| String-key hash | Python | 30.910 | 34.984 | 1.516 | 4.6% | 5/5 |
| String-key hash | Node.js | 9.833 | 13.624 | 1.530 | 13.7% | 5/5 |
| String-key hash | C# | 11.355 | 13.991 | 1.015 | 8.3% | 5/5 |
| Integer-key hash | AquariusLang | 80.875 | 128.739 | 19.161 | 18.2% | 5/5 |
| Integer-key hash | AquariusLang (typed) | 102.821 | 145.504 | 18.711 | 15.4% | 5/5 |
| Integer-key hash | AquariusLang (Native AOT compiler) | 87.048 | 121.409 | 13.040 | 12.5% | 5/5 |
| Integer-key hash | AquariusLang (typed, Native AOT compiler) | 83.257 | 106.855 | 10.111 | 10.0% | 5/5 |
| Integer-key hash | Python | 105.036 | 125.117 | 8.503 | 7.6% | 5/5 |
| Integer-key hash | Node.js | 30.351 | 39.526 | 3.542 | 10.3% | 5/5 |
| Integer-key hash | C# | 10.333 | 12.547 | 0.830 | 7.3% | 5/5 |
| Closures | AquariusLang | 93.557 | 103.627 | 4.580 | 4.7% | 5/5 |
| Closures | AquariusLang (typed) | 119.343 | 138.533 | 7.288 | 5.7% | 5/5 |
| Closures | AquariusLang (Native AOT compiler) | 90.599 | 104.960 | 5.975 | 5.9% | 5/5 |
| Closures | AquariusLang (typed, Native AOT compiler) | 114.316 | 126.826 | 4.659 | 3.8% | 5/5 |
| Closures | Python | 113.600 | 132.062 | 7.031 | 5.7% | 5/5 |
| Closures | Node.js | 14.500 | 20.154 | 2.379 | 14.9% | 5/5 |
| Closures | C# | 10.524 | 12.100 | 0.759 | 6.7% | 5/5 |
| Struct updates | AquariusLang | 64.126 | 80.112 | 6.725 | 9.6% | 5/5 |
| Struct updates | AquariusLang (typed) | 94.954 | 116.767 | 9.468 | 9.0% | 5/5 |
| Struct updates | AquariusLang (Native AOT compiler) | 69.281 | 77.424 | 3.188 | 4.3% | 5/5 |
| Struct updates | AquariusLang (typed, Native AOT compiler) | 101.615 | 106.672 | 1.984 | 1.9% | 5/5 |
| Struct updates | Python | 113.053 | 124.348 | 4.573 | 3.9% | 5/5 |
| Struct updates | Node.js | 3.893 | 5.368 | 0.547 | 11.9% | 5/5 |
| Struct updates | C# | 2.994 | 3.297 | 0.118 | 3.8% | 5/5 |
| Function calls | AquariusLang | 6.913 | 10.307 | 1.231 | 14.2% | 5/5 |
| Function calls | AquariusLang (typed) | 7.718 | 10.576 | 1.150 | 12.9% | 5/5 |
| Function calls | AquariusLang (Native AOT compiler) | 8.233 | 9.918 | 0.682 | 7.8% | 5/5 |
| Function calls | AquariusLang (typed, Native AOT compiler) | 8.005 | 10.218 | 0.926 | 10.4% | 5/5 |
| Function calls | Python | 122.857 | 146.372 | 9.857 | 7.3% | 5/5 |
| Function calls | Node.js | 8.322 | 10.627 | 0.998 | 10.6% | 5/5 |
| Function calls | C# | 6.424 | 7.353 | 0.408 | 6.0% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: Node.js 100.00, C# 51.23, AquariusLang 11.06, AquariusLang (Native AOT compiler) 10.95, AquariusLang (typed, Native AOT compiler) 9.90, AquariusLang (typed) 9.64, Python 7.81 (higher is faster).**

Pairwise composite speed: Node.js is 1.95× as fast as C#; Node.js is 9.04× as fast as AquariusLang; Node.js is 9.13× as fast as AquariusLang (Native AOT compiler); Node.js is 10.10× as fast as AquariusLang (typed, Native AOT compiler); Node.js is 10.38× as fast as AquariusLang (typed); Node.js is 12.81× as fast as Python; C# is 4.63× as fast as AquariusLang; C# is 4.68× as fast as AquariusLang (Native AOT compiler); C# is 5.17× as fast as AquariusLang (typed, Native AOT compiler); C# is 5.32× as fast as AquariusLang (typed); C# is 6.56× as fast as Python; AquariusLang is 1.01× as fast as AquariusLang (Native AOT compiler); AquariusLang is 1.12× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang is 1.15× as fast as AquariusLang (typed); AquariusLang is 1.42× as fast as Python; AquariusLang (Native AOT compiler) is 1.11× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (Native AOT compiler) is 1.14× as fast as AquariusLang (typed); AquariusLang (Native AOT compiler) is 1.40× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.03× as fast as AquariusLang (typed); AquariusLang (typed, Native AOT compiler) is 1.27× as fast as Python; AquariusLang (typed) is 1.23× as fast as Python.

| Rank | Language | Composite score | Speed vs Node.js | Speed vs C# | Speed vs AquariusLang | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs AquariusLang (typed) | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Node.js | 100.00 | 1.000× | 1.952× | 9.038× | 9.133× | 10.099× | 10.375× | 12.806× |
| 2 | C# | 51.23 | 0.512× | 1.000× | 4.630× | 4.679× | 5.174× | 5.315× | 6.561× |
| 3 | AquariusLang | 11.06 | 0.111× | 0.216× | 1.000× | 1.011× | 1.117× | 1.148× | 1.417× |
| 4 | AquariusLang (Native AOT compiler) | 10.95 | 0.109× | 0.214× | 0.990× | 1.000× | 1.106× | 1.136× | 1.402× |
| 5 | AquariusLang (typed, Native AOT compiler) | 9.90 | 0.099× | 0.193× | 0.895× | 0.904× | 1.000× | 1.027× | 1.268× |
| 6 | AquariusLang (typed) | 9.64 | 0.096× | 0.188× | 0.871× | 0.880× | 0.973× | 1.000× | 1.234× |
| 7 | Python | 7.81 | 0.078× | 0.152× | 0.706× | 0.713× | 0.789× | 0.810× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| String building | 20000 | 64.208 | 69.464 | 61.901 | 66.208 | 12.369 | 0.170 | 68.808 | 5.19× | 5.62× | 5.00× | 5.35× | 0.01× | 5.56× |
| String-key hash | 500000 | 36.571 | 37.035 | 35.464 | 37.540 | 31.790 | 8.781 | 10.499 | 1.15× | 1.17× | 1.12× | 1.18× | 0.28× | 0.33× |
| Integer-key hash | 1000000 | 99.462 | 112.715 | 110.934 | 106.503 | 125.116 | 34.492 | 11.009 | 0.79× | 0.90× | 0.89× | 0.85× | 0.28× | 0.09× |
| Closures | 1000000 | 96.000 | 113.815 | 94.302 | 103.015 | 120.136 | 15.170 | 8.055 | 0.80× | 0.95× | 0.78× | 0.86× | 0.13× | 0.07× |
| Struct updates | 1000000 | 67.823 | 99.335 | 68.277 | 99.093 | 118.252 | 3.610 | 2.825 | 0.57× | 0.84× | 0.58× | 0.84× | 0.03× | 0.02× |
| Function calls | 2000000 | 7.381 | 7.834 | 7.621 | 8.085 | 129.967 | 7.320 | 6.294 | 0.06× | 0.06× | 0.06× | 0.06× | 0.06× | 0.05× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| String building | 20000 | 69.464 | 0.170 | 0.00× | Node.js, 409.58× faster |
| String-key hash | 500000 | 37.035 | 8.781 | 0.24× | Node.js, 4.22× faster |
| Integer-key hash | 1000000 | 112.715 | 34.492 | 0.31× | Node.js, 3.27× faster |
| Closures | 1000000 | 113.815 | 15.170 | 0.13× | Node.js, 7.50× faster |
| Struct updates | 1000000 | 99.335 | 3.610 | 0.04× | Node.js, 27.52× faster |
| Function calls | 2000000 | 7.834 | 7.320 | 0.93× | Node.js, 1.07× faster |
| **Geometric mean** | | | | **0.10×** | Node.js, 10.38× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| String building | AquariusLang | 62.219 | 74.712 | 5.132 | 7.8% | 5/5 |
| String building | AquariusLang (typed) | 63.478 | 77.275 | 5.791 | 8.4% | 5/5 |
| String building | AquariusLang (Native AOT compiler) | 58.639 | 75.069 | 6.935 | 10.7% | 5/5 |
| String building | AquariusLang (typed, Native AOT compiler) | 61.206 | 74.225 | 5.237 | 7.8% | 5/5 |
| String building | Python | 11.849 | 15.189 | 1.590 | 12.1% | 5/5 |
| String building | Node.js | 0.160 | 0.178 | 0.007 | 4.1% | 5/5 |
| String building | C# | 62.561 | 87.445 | 9.432 | 13.2% | 5/5 |
| String-key hash | AquariusLang | 34.163 | 38.446 | 1.594 | 4.4% | 5/5 |
| String-key hash | AquariusLang (typed) | 35.808 | 43.740 | 3.152 | 8.2% | 5/5 |
| String-key hash | AquariusLang (Native AOT compiler) | 33.518 | 38.582 | 1.956 | 5.4% | 5/5 |
| String-key hash | AquariusLang (typed, Native AOT compiler) | 36.436 | 40.239 | 1.781 | 4.7% | 5/5 |
| String-key hash | Python | 31.271 | 35.151 | 1.565 | 4.8% | 5/5 |
| String-key hash | Node.js | 8.318 | 9.982 | 0.651 | 7.3% | 5/5 |
| String-key hash | C# | 9.607 | 11.608 | 0.789 | 7.5% | 5/5 |
| Integer-key hash | AquariusLang | 88.802 | 107.373 | 6.843 | 6.9% | 5/5 |
| Integer-key hash | AquariusLang (typed) | 103.280 | 123.279 | 7.937 | 7.0% | 5/5 |
| Integer-key hash | AquariusLang (Native AOT compiler) | 107.066 | 124.217 | 7.031 | 6.2% | 5/5 |
| Integer-key hash | AquariusLang (typed, Native AOT compiler) | 103.784 | 119.018 | 7.471 | 6.7% | 5/5 |
| Integer-key hash | Python | 109.674 | 130.018 | 8.078 | 6.5% | 5/5 |
| Integer-key hash | Node.js | 32.904 | 40.289 | 3.262 | 9.1% | 5/5 |
| Integer-key hash | C# | 10.463 | 12.592 | 0.834 | 7.4% | 5/5 |
| Closures | AquariusLang | 91.081 | 103.934 | 5.912 | 6.1% | 5/5 |
| Closures | AquariusLang (typed) | 102.704 | 121.090 | 8.215 | 7.4% | 5/5 |
| Closures | AquariusLang (Native AOT compiler) | 88.375 | 108.162 | 9.191 | 9.4% | 5/5 |
| Closures | AquariusLang (typed, Native AOT compiler) | 101.224 | 116.844 | 6.492 | 6.1% | 5/5 |
| Closures | Python | 114.484 | 124.765 | 3.659 | 3.1% | 5/5 |
| Closures | Node.js | 14.562 | 15.573 | 0.363 | 2.4% | 5/5 |
| Closures | C# | 7.033 | 8.691 | 0.619 | 7.8% | 5/5 |
| Struct updates | AquariusLang | 64.874 | 75.250 | 4.104 | 5.9% | 5/5 |
| Struct updates | AquariusLang (typed) | 92.121 | 106.585 | 5.515 | 5.6% | 5/5 |
| Struct updates | AquariusLang (Native AOT compiler) | 63.868 | 77.983 | 5.817 | 8.4% | 5/5 |
| Struct updates | AquariusLang (typed, Native AOT compiler) | 90.454 | 104.244 | 5.500 | 5.6% | 5/5 |
| Struct updates | Python | 111.844 | 121.902 | 4.193 | 3.6% | 5/5 |
| Struct updates | Node.js | 2.911 | 3.720 | 0.323 | 9.4% | 5/5 |
| Struct updates | C# | 2.751 | 3.203 | 0.214 | 7.3% | 5/5 |
| Function calls | AquariusLang | 7.051 | 10.253 | 1.347 | 17.1% | 5/5 |
| Function calls | AquariusLang (typed) | 7.348 | 8.080 | 0.289 | 3.7% | 5/5 |
| Function calls | AquariusLang (Native AOT compiler) | 6.429 | 9.094 | 1.059 | 14.1% | 5/5 |
| Function calls | AquariusLang (typed, Native AOT compiler) | 7.688 | 8.276 | 0.227 | 2.8% | 5/5 |
| Function calls | Python | 121.704 | 132.129 | 4.918 | 3.8% | 5/5 |
| Function calls | Node.js | 7.028 | 7.631 | 0.264 | 3.6% | 5/5 |
| Function calls | C# | 6.149 | 6.472 | 0.126 | 2.0% | 5/5 |

## AquariusLang compiler build and start times

Each AquariusLang candidate builds every program with its own `aqua` (`aqua build`) and runs it (`aqua run`). Workload timings exclude both; the table shows the median build time over every benchmark and mode, and per mode the median whole-process time (starting `aqua` and the runtime included).

| Candidate | Median build | Median process, standard mode | Median process, warmed mode |
| --- | ---: | ---: | ---: |
| AquariusLang | 208.1 ms | 197.3 ms | 815.8 ms |
| AquariusLang (typed) | 196.3 ms | 250.0 ms | 939.6 ms |
| AquariusLang (Native AOT compiler) | 45.8 ms | 143.4 ms | 774.2 ms |
| AquariusLang (typed, Native AOT compiler) | 44.5 ms | 171.6 ms | 884.9 ms |

## How the composite score is computed

For each mode, the relative speeds on this run's 6 algorithms are combined with equal weights as a geometric mean, and the fastest language is set to 100. Timing uses each language's in-process monotonic timer and covers data initialization and the algorithm and checksum, excluding process start, source or Wasm loading and initial compilation, and output.

Relative speed G = geometric mean (Python median time ÷ the language's median time, per benchmark); composite score = 100 × G ÷ the largest G among all 7 languages, so the top score is always 100. Every algorithm has the same weight; a mode gets composite scores only when all 7 languages pass every selected test in that mode. Scores from different modes, test sets or input sizes cannot be compared directly.

In the ranking tables, speed = the row language's composite score ÷ the column's baseline language's composite score, computed from unrounded scores; above 1 is faster than that baseline, below 1 slower.

## Running

Requirements: Python 3.10 or later, Node.js, .NET 8 SDK (with the net8.0 targeting pack and runtime), and an AquariusLang Wasm compiler that supports `目前時間()` / `currentTime()` (`aqua` with its bundled files). No Python packages or npm install are needed. The AquariusLang scripts use the Traditional Chinese keywords and bilingual built-ins of AquariusLang's Traditional Chinese edition, so the older English-only interpreter cannot run them.

```powershell
python run_benchmarks.py
# Small inputs, a quick correctness check:
python run_benchmarks.py --profile smoke --repetitions 1 --warmups 0
# Larger inputs, reducing the effect of JIT warm-up:
python run_benchmarks.py --profile large --timeout 300
# Warmed mode only, with custom in-process warm-up and timed run counts:
python run_benchmarks.py --modes warmed --in-process-warmups 10 --in-process-runs 7
# Executable paths, when needed:
python run_benchmarks.py --aquarius "C:\Aquarius\aqua.exe" --node "C:\Program Files\nodejs\node.exe" --dotnet "C:\Program Files\dotnet\dotnet.exe"
# Selected algorithms only:
python run_benchmarks.py --benchmarks fibonacci sieve matrix
# Regenerate the READMEs from saved data, without measuring:
python run_benchmarks.py --report-only results/latest.json
# Run the harness and reference-answer tests:
python -m unittest discover -s tests -v
```

If `python` is a pyenv shim with no version set, call the installed `python.exe` directly. The harness runs the Python tests with its own interpreter by default; `--python PATH` selects another. It searches the current process's PATH, and on Windows also the latest user and system PATH, so an older terminal session still finds a newly added AquariusLang path. Runtime options take a single executable path. C# prefers a dotnet that has the SDK and also searches DOTNET_ROOT and the user's `.dotnet` folder; `--dotnet PATH` selects one.

To run one C# test on its own (the sieve, for example):

```powershell
dotnet run --project benchmarks/csharp/Benchmark.csproj --configuration Release -p:BenchmarkSource=sieve.cs
```

For each mode the harness copies the sources into a temporary folder and replaces only three declarations: `benchmark_n` (input size), `benchmark_warmups` (in-process warm-up runs) and `benchmark_timed_runs` (in-process timed runs). Running a script directly uses the standard size and standard mode (no warm-up, one timed run). Each measurement creates a dated subfolder of `results/` and regenerates `results/latest.json`, `README.md` (English) and `README.tw.md` (Traditional Chinese). `--modes` selects the modes (both `standard warmed` by default); `--in-process-warmups` (default 5) and `--in-process-runs` (default 5) set the in-process counts of warmed mode; `--repetitions` is the number of processes per case that count toward the statistics, and `--warmups` the number of discarded warm-up processes per case. `--output-dir`, `--readme` (the English README's path; the Traditional Chinese one is written beside it as `.tw.md`), `--timeout` and `--seed` customize a run further. Exit code 1 means at least one runtime was unavailable or a test failed validation; the report still keeps the failure details.

## Methodology

- Every sample starts a new process, but the ranking uses only the `ELAPSED_MS` each script reports itself. AquariusLang uses `目前時間()` (`currentTime()`, milliseconds), Python `time.perf_counter_ns()` (nanosecond difference ÷ 1e6), Node.js `process.hrtime.bigint()` (nanosecond difference ÷ 1e6), C# `Stopwatch.GetTimestamp()` (tick difference × 1000 ÷ Frequency). All timers are monotonic.
- All 7 languages start timing after the function definitions and before data initialization, and stop after the algorithm and checksum, before output. Memory allocation, garbage collection and on-demand JIT during the run still count. `elapsed_ms` in the JSON and CSV is the process value (the median of the in-process timed runs; `run_elapsed_ms` keeps each run); `process_elapsed_ms` also keeps the whole-process time for diagnosis and takes no part in the statistics or ranking.
- Standard mode: Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.
- Warmed mode: Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.
- Each script wraps the timed work in a `benchmark_run` function; in-process warm-up only calls that function more often and changes neither the algorithm nor the timed interval.
- AquariusLang always builds the Wasm with `aqua build` before measuring, then runs `aqua run`; Wasm generation is not part of the sample time, and each mode's copy is built separately. "AquariusLang (typed)" uses the same compiler and the same algorithms, adding only optional type annotations on variables, parameters and return values (`benchmarks/aquarius_typed/`); typed functions must declare a return type, so the in-place functions of quicksort and spectral norm gain a `回傳 0;` (`return 0;`) line, and binary trees annotate the tree arrays as `陣列` (`Array`, an array whose elements can be any value). The input size `benchmark_n` is declared `常數` (`const`), the counterpart of C#'s `static readonly int benchmark_n`, which the JIT treats as a constant; this needs a compiler that supports `常數`, and the untyped scripts keep `變數`. Python runs the source, and Node.js uses V8. C# is compiled ahead of time into a net8.0 assembly with `dotnet build --configuration Release` and run directly as `dotnet Benchmark.dll`; build and restore are not timed, and no external NuGet packages are used. The initial JIT before Main is not timed; on-demand JIT inside the timed interval still counts. The assembly turns tiered compilation off (`TieredCompilation=false`), so each method is compiled by the optimizing JIT on its first call, matching the optimized Wasmtime compilation AquariusLang finishes before timing. No NumPy, native algorithm libraries, worker threads or built-in sorts are used.
- Warm-up process samples are discarded; they warm the operating system's file cache, and no JIT or VM state carries over between processes. Each round shuffles every algorithm, language and mode combination with the recorded random seed, then runs them in that order.
- Every timed run of every warm-up and counted sample must match the untimed Python reference answer. Integers must be identical; the squared spectral norm allows a relative error of 1e-9 and an absolute error of 1e-12. A non-zero exit code, a timeout, missing or extra standard output, a non-finite value or a checksum mismatch fails the test. The timing output must be a finite millisecond value above zero; a missing timing does not fall back to whole-process timing.
- AquariusLang's integer `/` truncates; Python uses `//` and Node.js `Math.trunc` to match. Floating-point tests use double precision (AquariusLang uses `d` literals); at the standard size every intermediate integer stays within the signed 32-bit range.
- Array construction has the same linear cost in every language: AquariusLang preallocates with `陣列.建立` (`Array.Make`; quicksort uses `陣列.追加`, `Array.Append`, with reserved capacity), Python uses `[value] * n` / `append`, Node.js `push`, C# `new T[n]` (with `Array.Fill` where needed); no append that copies the whole array each time is used.
- Compilation timing: Wasmtime has fully compiled the AquariusLang Wasm to machine code before timing starts. C# has tiered compilation off, so methods are compiled by the optimizing JIT on their first call; in standard mode that JIT is still inside the timed interval. Node.js (V8) cannot optimize ahead of time and starts in its interpreter and baseline compiler; in standard mode hot functions are optimized inside the timed interval, which favors AquariusLang; warmed mode relies on in-process warm-up to optimize hot functions before timing, though a little JIT or garbage collection may still fall inside the timed interval. At the standard size each test takes about 1 millisecond, so timer and allocation noise weigh more; `--profile large` reduces this with larger inputs, and the scores of the two sizes must not be mixed.
- Small workloads can be affected by timer and function call costs; warmed mode warms up only a few times and is not the steady-state speed of a long run, while standard mode reflects only the first run; neither represents a language ranking for every program. CPU frequency, temperature, background work and scheduling noise are not controlled. Process memory use and CPU time are not measured; the RAM below is the machine's installed memory.

## Test date and environment

- Started: 2026-11-18T14:09:48.930889+08:00
- Finished: 2026-11-18T14:13:58.824061+08:00
- Time zone: Asia/Taipei
- Input size: large (`large`); 5 counted and 1 discarded warm-up processes per case
- Modes: Standard mode (cold start, one timed run per process); Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)
- Order random seed: 20261010; timeout per process: 120 s
- Operating system: Windows-11-10.0.26200-SP0
- Architecture: AMD64
- CPU: 13th Gen Intel(R) Core(TM) i9-13900H; logical processors: 20
- Physical RAM: 31.71 GiB
- Active power plan: Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced)
- Python harness version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- Process CPU affinity mask: `0xfffff`
- Harness diagnostic timer resolution: 1e-07 s (not the resolution of every language's timer)

| Runtime | Version / build | Executable |
| --- | --- | --- |
| AquariusLang | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua-r2r\aqua.exe |
| AquariusLang (typed) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua-r2r\aqua.exe |
| AquariusLang (Native AOT compiler) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua-aot\aqua.exe |
| AquariusLang (typed, Native AOT compiler) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua-aot\aqua.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.exe |
| C# | SDKs: 8.0.426 [C:\Program Files\dotnet\sdk] Runtimes: Microsoft.AspNetCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App] Microsoft.NETCore.App 6.0.36 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.WindowsDesktop.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] Microsoft.WindowsDesktop.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] | C:\Program Files\dotnet\dotnet.exe |

AquariusLang release folder: `C:\OfficialProjects\AquariusLangTW\dist\aqua-r2r`.

AquariusLang launcher SHA-256: `dce3a51e600feaee88a3985a5c60eaf197066f98cf9913f2be8c6ec86d5b7d33`.


## Correctness

Every warm-up and counted sample output, in every language and mode, matches the Python reference answer.

| Benchmark | Expected result | Workload |
| --- | ---: | --- |
| String building | 60000 | Appends "ab," n times to a string that a closure can also see; returns its length. |
| String-key hash | 501000 | n count updates (one read, one write) over 1000 string keys. |
| Integer-key hash | 200003 | Inserts n / 5 integer keys, then reads n times. |
| Closures | 999993 | Maps n elements with a function literal, then calls a closure that updates a captured variable n times. |
| Struct updates | 27797 | n calls of a step function on 1000 struct particles taken from an array. |
| Function calls | 235197 | n calls of a small two-argument function. |

## Reproducible data

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261118-140948-930889\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261118-140948-930889\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261118-140948-930889\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/aquarius_aot/`, `benchmarks/aquarius_typed_aot/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

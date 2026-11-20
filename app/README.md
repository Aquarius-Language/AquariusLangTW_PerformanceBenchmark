# Desktop performance benchmark: AquariusLang, AquariusLang (typed), AquariusLang (Native AOT compiler), AquariusLang (typed, Native AOT compiler), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: Node.js 100.00, C# 60.54, AquariusLang (typed) 18.80, AquariusLang (typed, Native AOT compiler) 18.51, AquariusLang (Native AOT compiler) 14.35, AquariusLang 14.25, Python 10.45
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: Node.js 100.00, C# 49.96, AquariusLang (typed, Native AOT compiler) 14.09, AquariusLang (typed) 13.92, AquariusLang (Native AOT compiler) 11.11, AquariusLang 11.10, Python 7.45

This is the app suite: 6 operations everyday programs use (hashes, strings, closures, structs and calls), 42 standalone programs, run with `run_benchmarks.py --suite app`. The ten classic algorithms are in [../README.md](../README.md).

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: Node.js 100.00, C# 60.54, AquariusLang (typed) 18.80, AquariusLang (typed, Native AOT compiler) 18.51, AquariusLang (Native AOT compiler) 14.35, AquariusLang 14.25, Python 10.45 (higher is faster).**

Pairwise composite speed: Node.js is 1.65× as fast as C#; Node.js is 5.32× as fast as AquariusLang (typed); Node.js is 5.40× as fast as AquariusLang (typed, Native AOT compiler); Node.js is 6.97× as fast as AquariusLang (Native AOT compiler); Node.js is 7.02× as fast as AquariusLang; Node.js is 9.57× as fast as Python; C# is 3.22× as fast as AquariusLang (typed); C# is 3.27× as fast as AquariusLang (typed, Native AOT compiler); C# is 4.22× as fast as AquariusLang (Native AOT compiler); C# is 4.25× as fast as AquariusLang; C# is 5.79× as fast as Python; AquariusLang (typed) is 1.02× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (typed) is 1.31× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 1.32× as fast as AquariusLang; AquariusLang (typed) is 1.80× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.29× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 1.30× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 1.77× as fast as Python; AquariusLang (Native AOT compiler) is 1.01× as fast as AquariusLang; AquariusLang (Native AOT compiler) is 1.37× as fast as Python; AquariusLang is 1.36× as fast as Python.

| Rank | Language | Composite score | Speed vs Node.js | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Node.js | 100.00 | 1.000× | 1.652× | 5.319× | 5.402× | 6.968× | 7.016× | 9.566× |
| 2 | C# | 60.54 | 0.605× | 1.000× | 3.220× | 3.270× | 4.218× | 4.247× | 5.791× |
| 3 | AquariusLang (typed) | 18.80 | 0.188× | 0.311× | 1.000× | 1.016× | 1.310× | 1.319× | 1.798× |
| 4 | AquariusLang (typed, Native AOT compiler) | 18.51 | 0.185× | 0.306× | 0.985× | 1.000× | 1.290× | 1.299× | 1.771× |
| 5 | AquariusLang (Native AOT compiler) | 14.35 | 0.144× | 0.237× | 0.763× | 0.775× | 1.000× | 1.007× | 1.373× |
| 6 | AquariusLang | 14.25 | 0.143× | 0.235× | 0.758× | 0.770× | 0.993× | 1.000× | 1.363× |
| 7 | Python | 10.45 | 0.105× | 0.173× | 0.556× | 0.565× | 0.728× | 0.733× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| String building | 20000 | 62.842 | 57.080 | 64.284 | 58.405 | 11.191 | 0.521 | 61.111 | 5.62× | 5.10× | 5.74× | 5.22× | 0.05× | 5.46× |
| String-key hash | 500000 | 32.119 | 34.420 | 31.069 | 33.859 | 30.717 | 10.084 | 10.523 | 1.05× | 1.12× | 1.01× | 1.10× | 0.33× | 0.34× |
| Integer-key hash | 1000000 | 71.519 | 73.759 | 69.957 | 78.203 | 101.273 | 30.798 | 10.550 | 0.71× | 0.73× | 0.69× | 0.77× | 0.30× | 0.10× |
| Closures | 1000000 | 97.391 | 103.893 | 97.105 | 100.759 | 108.566 | 13.993 | 10.648 | 0.90× | 0.96× | 0.89× | 0.93× | 0.13× | 0.10× |
| Struct updates | 1000000 | 69.456 | 14.810 | 69.151 | 15.810 | 109.340 | 3.935 | 2.926 | 0.64× | 0.14× | 0.63× | 0.14× | 0.04× | 0.03× |
| Function calls | 2000000 | 7.986 | 6.644 | 7.977 | 6.598 | 121.236 | 7.344 | 6.285 | 0.07× | 0.05× | 0.07× | 0.05× | 0.06× | 0.05× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| String building | 20000 | 57.080 | 0.521 | 0.01× | Node.js, 109.62× faster |
| String-key hash | 500000 | 34.420 | 10.084 | 0.29× | Node.js, 3.41× faster |
| Integer-key hash | 1000000 | 73.759 | 30.798 | 0.42× | Node.js, 2.39× faster |
| Closures | 1000000 | 103.893 | 13.993 | 0.13× | Node.js, 7.42× faster |
| Struct updates | 1000000 | 14.810 | 3.935 | 0.27× | Node.js, 3.76× faster |
| Function calls | 2000000 | 6.644 | 7.344 | 1.11× | AquariusLang (typed), 1.11× faster |
| **Geometric mean** | | | | **0.19×** | Node.js, 5.32× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| String building | AquariusLang | 57.183 | 68.307 | 4.094 | 6.5% | 5/5 |
| String building | AquariusLang (typed) | 54.535 | 59.049 | 1.890 | 3.3% | 5/5 |
| String building | AquariusLang (Native AOT compiler) | 55.749 | 66.156 | 4.240 | 6.7% | 5/5 |
| String building | AquariusLang (typed, Native AOT compiler) | 55.026 | 62.178 | 2.660 | 4.5% | 5/5 |
| String building | Python | 10.582 | 11.865 | 0.534 | 4.8% | 5/5 |
| String building | Node.js | 0.459 | 0.528 | 0.031 | 6.2% | 5/5 |
| String building | C# | 54.867 | 66.951 | 5.045 | 8.2% | 5/5 |
| String-key hash | AquariusLang | 29.897 | 35.883 | 2.281 | 7.0% | 5/5 |
| String-key hash | AquariusLang (typed) | 31.142 | 41.340 | 4.325 | 11.9% | 5/5 |
| String-key hash | AquariusLang (Native AOT compiler) | 30.128 | 35.412 | 2.341 | 7.2% | 5/5 |
| String-key hash | AquariusLang (typed, Native AOT compiler) | 30.866 | 39.071 | 3.401 | 10.0% | 5/5 |
| String-key hash | Python | 30.169 | 33.037 | 1.191 | 3.8% | 5/5 |
| String-key hash | Node.js | 8.634 | 10.223 | 0.682 | 7.0% | 5/5 |
| String-key hash | C# | 9.724 | 12.320 | 0.953 | 8.9% | 5/5 |
| Integer-key hash | AquariusLang | 68.222 | 81.607 | 5.194 | 7.1% | 5/5 |
| Integer-key hash | AquariusLang (typed) | 71.804 | 91.083 | 7.879 | 10.1% | 5/5 |
| Integer-key hash | AquariusLang (Native AOT compiler) | 67.242 | 79.936 | 5.829 | 8.0% | 5/5 |
| Integer-key hash | AquariusLang (typed, Native AOT compiler) | 74.861 | 85.038 | 3.927 | 5.0% | 5/5 |
| Integer-key hash | Python | 94.772 | 119.944 | 10.090 | 9.8% | 5/5 |
| Integer-key hash | Node.js | 28.159 | 46.139 | 7.272 | 21.8% | 5/5 |
| Integer-key hash | C# | 9.992 | 11.299 | 0.486 | 4.6% | 5/5 |
| Closures | AquariusLang | 87.578 | 102.178 | 6.102 | 6.4% | 5/5 |
| Closures | AquariusLang (typed) | 102.042 | 118.338 | 6.959 | 6.5% | 5/5 |
| Closures | AquariusLang (Native AOT compiler) | 90.969 | 103.404 | 4.608 | 4.7% | 5/5 |
| Closures | AquariusLang (typed, Native AOT compiler) | 98.897 | 110.124 | 4.635 | 4.5% | 5/5 |
| Closures | Python | 104.945 | 113.977 | 3.354 | 3.1% | 5/5 |
| Closures | Node.js | 13.206 | 15.017 | 0.667 | 4.7% | 5/5 |
| Closures | C# | 9.525 | 11.635 | 0.885 | 8.5% | 5/5 |
| Struct updates | AquariusLang | 63.196 | 72.928 | 4.509 | 6.6% | 5/5 |
| Struct updates | AquariusLang (typed) | 13.103 | 17.457 | 1.718 | 11.2% | 5/5 |
| Struct updates | AquariusLang (Native AOT compiler) | 66.008 | 70.817 | 1.745 | 2.5% | 5/5 |
| Struct updates | AquariusLang (typed, Native AOT compiler) | 14.049 | 17.406 | 1.463 | 9.2% | 5/5 |
| Struct updates | Python | 104.014 | 121.092 | 7.086 | 6.4% | 5/5 |
| Struct updates | Node.js | 3.893 | 5.136 | 0.531 | 12.7% | 5/5 |
| Struct updates | C# | 2.699 | 2.991 | 0.120 | 4.1% | 5/5 |
| Function calls | AquariusLang | 7.131 | 10.566 | 1.292 | 15.4% | 5/5 |
| Function calls | AquariusLang (typed) | 6.035 | 7.178 | 0.471 | 7.1% | 5/5 |
| Function calls | AquariusLang (Native AOT compiler) | 6.421 | 8.138 | 0.708 | 9.3% | 5/5 |
| Function calls | AquariusLang (typed, Native AOT compiler) | 6.293 | 8.165 | 0.845 | 12.0% | 5/5 |
| Function calls | Python | 117.162 | 124.823 | 3.619 | 3.0% | 5/5 |
| Function calls | Node.js | 7.053 | 7.660 | 0.233 | 3.2% | 5/5 |
| Function calls | C# | 5.607 | 6.505 | 0.423 | 6.9% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: Node.js 100.00, C# 49.96, AquariusLang (typed, Native AOT compiler) 14.09, AquariusLang (typed) 13.92, AquariusLang (Native AOT compiler) 11.11, AquariusLang 11.10, Python 7.45 (higher is faster).**

Pairwise composite speed: Node.js is 2.00× as fast as C#; Node.js is 7.10× as fast as AquariusLang (typed, Native AOT compiler); Node.js is 7.18× as fast as AquariusLang (typed); Node.js is 9.00× as fast as AquariusLang (Native AOT compiler); Node.js is 9.01× as fast as AquariusLang; Node.js is 13.41× as fast as Python; C# is 3.55× as fast as AquariusLang (typed, Native AOT compiler); C# is 3.59× as fast as AquariusLang (typed); C# is 4.50× as fast as AquariusLang (Native AOT compiler); C# is 4.50× as fast as AquariusLang; C# is 6.70× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.01× as fast as AquariusLang (typed); AquariusLang (typed, Native AOT compiler) is 1.27× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 1.27× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 1.89× as fast as Python; AquariusLang (typed) is 1.25× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 1.25× as fast as AquariusLang; AquariusLang (typed) is 1.87× as fast as Python; AquariusLang (Native AOT compiler) is 1.00× as fast as AquariusLang; AquariusLang (Native AOT compiler) is 1.49× as fast as Python; AquariusLang is 1.49× as fast as Python.

| Rank | Language | Composite score | Speed vs Node.js | Speed vs C# | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs AquariusLang (typed) | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Node.js | 100.00 | 1.000× | 2.002× | 7.097× | 7.183× | 9.004× | 9.007× | 13.414× |
| 2 | C# | 49.96 | 0.500× | 1.000× | 3.546× | 3.589× | 4.498× | 4.500× | 6.702× |
| 3 | AquariusLang (typed, Native AOT compiler) | 14.09 | 0.141× | 0.282× | 1.000× | 1.012× | 1.269× | 1.269× | 1.890× |
| 4 | AquariusLang (typed) | 13.92 | 0.139× | 0.279× | 0.988× | 1.000× | 1.254× | 1.254× | 1.868× |
| 5 | AquariusLang (Native AOT compiler) | 11.11 | 0.111× | 0.222× | 0.788× | 0.798× | 1.000× | 1.000× | 1.490× |
| 6 | AquariusLang | 11.10 | 0.111× | 0.222× | 0.788× | 0.797× | 1.000× | 1.000× | 1.489× |
| 7 | Python | 7.45 | 0.075× | 0.149× | 0.529× | 0.535× | 0.671× | 0.671× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| String building | 20000 | 55.951 | 58.012 | 57.202 | 57.006 | 11.137 | 0.150 | 56.019 | 5.02× | 5.21× | 5.14× | 5.12× | 0.01× | 5.03× |
| String-key hash | 500000 | 30.405 | 29.723 | 30.374 | 30.466 | 31.086 | 7.945 | 9.818 | 0.98× | 0.96× | 0.98× | 0.98× | 0.26× | 0.32× |
| Integer-key hash | 1000000 | 74.831 | 67.307 | 73.233 | 66.334 | 105.338 | 29.306 | 9.158 | 0.71× | 0.64× | 0.70× | 0.63× | 0.28× | 0.09× |
| Closures | 1000000 | 89.734 | 103.785 | 89.671 | 101.107 | 110.331 | 13.991 | 6.802 | 0.81× | 0.94× | 0.81× | 0.92× | 0.13× | 0.06× |
| Struct updates | 1000000 | 63.857 | 14.919 | 63.259 | 14.738 | 106.307 | 2.841 | 2.705 | 0.60× | 0.14× | 0.60× | 0.14× | 0.03× | 0.03× |
| Function calls | 2000000 | 6.422 | 6.706 | 6.477 | 6.534 | 119.534 | 6.304 | 6.090 | 0.05× | 0.06× | 0.05× | 0.05× | 0.05× | 0.05× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| String building | 20000 | 58.012 | 0.150 | 0.00× | Node.js, 385.72× faster |
| String-key hash | 500000 | 29.723 | 7.945 | 0.27× | Node.js, 3.74× faster |
| Integer-key hash | 1000000 | 67.307 | 29.306 | 0.44× | Node.js, 2.30× faster |
| Closures | 1000000 | 103.785 | 13.991 | 0.13× | Node.js, 7.42× faster |
| Struct updates | 1000000 | 14.919 | 2.841 | 0.19× | Node.js, 5.25× faster |
| Function calls | 2000000 | 6.706 | 6.304 | 0.94× | Node.js, 1.06× faster |
| **Geometric mean** | | | | **0.14×** | Node.js, 7.18× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| String building | AquariusLang | 52.861 | 62.845 | 3.992 | 7.0% | 5/5 |
| String building | AquariusLang (typed) | 53.420 | 62.032 | 3.625 | 6.3% | 5/5 |
| String building | AquariusLang (Native AOT compiler) | 51.898 | 65.029 | 4.815 | 8.4% | 5/5 |
| String building | AquariusLang (typed, Native AOT compiler) | 54.079 | 61.401 | 2.679 | 4.7% | 5/5 |
| String building | Python | 10.261 | 11.922 | 0.669 | 6.1% | 5/5 |
| String building | Node.js | 0.125 | 0.175 | 0.019 | 12.5% | 5/5 |
| String building | C# | 53.924 | 67.529 | 5.447 | 9.3% | 5/5 |
| String-key hash | AquariusLang | 30.329 | 32.639 | 1.009 | 3.3% | 5/5 |
| String-key hash | AquariusLang (typed) | 29.054 | 31.078 | 0.885 | 3.0% | 5/5 |
| String-key hash | AquariusLang (Native AOT compiler) | 28.863 | 30.629 | 0.708 | 2.4% | 5/5 |
| String-key hash | AquariusLang (typed, Native AOT compiler) | 29.229 | 30.817 | 0.705 | 2.3% | 5/5 |
| String-key hash | Python | 30.126 | 32.187 | 0.760 | 2.4% | 5/5 |
| String-key hash | Node.js | 7.394 | 8.429 | 0.431 | 5.4% | 5/5 |
| String-key hash | C# | 9.421 | 11.277 | 0.720 | 7.1% | 5/5 |
| Integer-key hash | AquariusLang | 67.812 | 92.103 | 9.971 | 13.0% | 5/5 |
| Integer-key hash | AquariusLang (typed) | 61.860 | 71.605 | 4.062 | 6.0% | 5/5 |
| Integer-key hash | AquariusLang (Native AOT compiler) | 68.521 | 82.578 | 5.626 | 7.6% | 5/5 |
| Integer-key hash | AquariusLang (typed, Native AOT compiler) | 63.448 | 71.863 | 3.197 | 4.7% | 5/5 |
| Integer-key hash | Python | 99.802 | 132.961 | 13.392 | 12.1% | 5/5 |
| Integer-key hash | Node.js | 27.591 | 29.539 | 0.787 | 2.7% | 5/5 |
| Integer-key hash | C# | 8.702 | 10.689 | 0.825 | 8.7% | 5/5 |
| Closures | AquariusLang | 88.359 | 93.190 | 1.859 | 2.1% | 5/5 |
| Closures | AquariusLang (typed) | 97.449 | 104.549 | 3.218 | 3.2% | 5/5 |
| Closures | AquariusLang (Native AOT compiler) | 87.156 | 93.045 | 2.609 | 2.9% | 5/5 |
| Closures | AquariusLang (typed, Native AOT compiler) | 94.748 | 104.844 | 3.816 | 3.8% | 5/5 |
| Closures | Python | 107.443 | 112.790 | 2.019 | 1.8% | 5/5 |
| Closures | Node.js | 12.759 | 14.161 | 0.570 | 4.2% | 5/5 |
| Closures | C# | 6.718 | 7.819 | 0.472 | 6.7% | 5/5 |
| Struct updates | AquariusLang | 61.661 | 71.103 | 3.796 | 5.9% | 5/5 |
| Struct updates | AquariusLang (typed) | 14.451 | 15.933 | 0.544 | 3.6% | 5/5 |
| Struct updates | AquariusLang (Native AOT compiler) | 62.067 | 64.660 | 1.044 | 1.7% | 5/5 |
| Struct updates | AquariusLang (typed, Native AOT compiler) | 14.636 | 15.024 | 0.152 | 1.0% | 5/5 |
| Struct updates | Python | 104.086 | 110.823 | 2.456 | 2.3% | 5/5 |
| Struct updates | Node.js | 2.723 | 4.018 | 0.541 | 17.5% | 5/5 |
| Struct updates | C# | 2.451 | 2.745 | 0.130 | 4.9% | 5/5 |
| Function calls | AquariusLang | 6.012 | 6.910 | 0.335 | 5.2% | 5/5 |
| Function calls | AquariusLang (typed) | 6.033 | 7.443 | 0.528 | 7.9% | 5/5 |
| Function calls | AquariusLang (Native AOT compiler) | 6.387 | 7.238 | 0.364 | 5.5% | 5/5 |
| Function calls | AquariusLang (typed, Native AOT compiler) | 6.031 | 6.788 | 0.316 | 4.9% | 5/5 |
| Function calls | Python | 115.897 | 125.227 | 3.431 | 2.9% | 5/5 |
| Function calls | Node.js | 6.025 | 7.734 | 0.687 | 10.5% | 5/5 |
| Function calls | C# | 5.889 | 6.478 | 0.229 | 3.7% | 5/5 |

## AquariusLang compiler build and start times

Each AquariusLang candidate builds every program with its own `aqua` (`aqua build`) and runs it (`aqua run`). Workload timings exclude both; the table shows the median build time over every benchmark and mode, and per mode the median whole-process time (starting `aqua` and the runtime included).

| Candidate | Median build | Median process, standard mode | Median process, warmed mode |
| --- | ---: | ---: | ---: |
| AquariusLang | 178.4 ms | 189.0 ms | 745.2 ms |
| AquariusLang (typed) | 196.7 ms | 166.5 ms | 568.8 ms |
| AquariusLang (Native AOT compiler) | 41.8 ms | 134.9 ms | 717.6 ms |
| AquariusLang (typed, Native AOT compiler) | 38.1 ms | 114.9 ms | 510.7 ms |

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

- Started: 2026-11-20T17:50:00.370526+08:00
- Finished: 2026-11-20T17:53:16.515865+08:00
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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261120-175000-370526\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261120-175000-370526\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\app\20261120-175000-370526\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/aquarius_aot/`, `benchmarks/aquarius_typed_aot/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

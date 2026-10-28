# Desktop performance benchmark: AquariusLang, AquariusLang (typed), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

> **Note: at the standard size most tests take about 1 millisecond, so the results mainly reflect a short program's latency after start-up (JIT warm-up, initial memory allocation), not sustained speed. To compare language speed, use `--profile large`.**

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: AquariusLang (typed) 100.00, AquariusLang 81.70, C# 59.14, Node.js 25.55, Python 4.65
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 50.50, AquariusLang 39.48, Node.js 39.08, Python 2.26

The project provides ten classic algorithms, 50 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: AquariusLang (typed) 100.00, AquariusLang 81.70, C# 59.14, Node.js 25.55, Python 4.65 (higher is faster).**

Pairwise composite speed: AquariusLang (typed) is 1.22× as fast as AquariusLang; AquariusLang (typed) is 1.69× as fast as C#; AquariusLang (typed) is 3.91× as fast as Node.js; AquariusLang (typed) is 21.51× as fast as Python; AquariusLang is 1.38× as fast as C#; AquariusLang is 3.20× as fast as Node.js; AquariusLang is 17.57× as fast as Python; C# is 2.32× as fast as Node.js; C# is 12.72× as fast as Python; Node.js is 5.49× as fast as Python.

| Rank | Language | Composite score | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs C# | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | AquariusLang (typed) | 100.00 | 1.000× | 1.224× | 1.691× | 3.914× | 21.507× |
| 2 | AquariusLang | 81.70 | 0.817× | 1.000× | 1.381× | 3.198× | 17.571× |
| 3 | C# | 59.14 | 0.591× | 0.724× | 1.000× | 2.315× | 12.720× |
| 4 | Node.js | 25.55 | 0.255× | 0.313× | 0.432× | 1.000× | 5.494× |
| 5 | Python | 4.65 | 0.046× | 0.057× | 0.079× | 0.182× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 28 | 1.523 | 1.601 | 29.279 | 2.411 | 0.827 | 0.05× | 0.05× | 0.08× | 0.03× |
| Ackermann function | 6 | 0.558 | 0.560 | 11.196 | 0.675 | 0.236 | 0.05× | 0.05× | 0.06× | 0.02× |
| Sieve of Eratosthenes | 10000 | 0.071 | 0.036 | 0.576 | 0.553 | 0.385 | 0.12× | 0.06× | 0.96× | 0.67× |
| Quicksort | 2000 | 0.258 | 0.125 | 1.347 | 0.855 | 0.555 | 0.19× | 0.09× | 0.63× | 0.41× |
| Matrix multiplication | 45 | 0.218 | 0.133 | 5.561 | 1.396 | 0.299 | 0.04× | 0.02× | 0.25× | 0.05× |
| Mandelbrot set | 80 | 0.321 | 0.319 | 9.958 | 1.022 | 0.384 | 0.03× | 0.03× | 0.10× | 0.04× |
| N-Queens | 8 | 0.231 | 0.201 | 3.731 | 0.685 | 0.386 | 0.06× | 0.05× | 0.18× | 0.10× |
| Binary trees | 12 | 1.986 | 2.037 | 9.490 | 2.911 | 1.434 | 0.21× | 0.21× | 0.31× | 0.15× |
| Spectral norm | 60 | 0.287 | 0.263 | 19.466 | 1.740 | 1.184 | 0.01× | 0.01× | 0.09× | 0.06× |
| Collatz conjecture | 10000 | 1.231 | 1.267 | 51.028 | 5.192 | 1.421 | 0.02× | 0.02× | 0.10× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 28 | 1.601 | 2.411 | 1.51× | AquariusLang (typed), 1.51× faster |
| Ackermann function | 6 | 0.560 | 0.675 | 1.21× | AquariusLang (typed), 1.21× faster |
| Sieve of Eratosthenes | 10000 | 0.036 | 0.553 | 15.27× | AquariusLang (typed), 15.27× faster |
| Quicksort | 2000 | 0.125 | 0.855 | 6.85× | AquariusLang (typed), 6.85× faster |
| Matrix multiplication | 45 | 0.133 | 1.396 | 10.51× | AquariusLang (typed), 10.51× faster |
| Mandelbrot set | 80 | 0.319 | 1.022 | 3.20× | AquariusLang (typed), 3.20× faster |
| N-Queens | 8 | 0.201 | 0.685 | 3.40× | AquariusLang (typed), 3.40× faster |
| Binary trees | 12 | 2.037 | 2.911 | 1.43× | AquariusLang (typed), 1.43× faster |
| Spectral norm | 60 | 0.263 | 1.740 | 6.62× | AquariusLang (typed), 6.62× faster |
| Collatz conjecture | 10000 | 1.267 | 5.192 | 4.10× | AquariusLang (typed), 4.10× faster |
| **Geometric mean** | | | | **3.91×** | AquariusLang (typed), 3.91× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 1.477 | 1.657 | 0.078 | 5.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 1.513 | 2.716 | 0.547 | 28.1% | 5/5 |
| Recursive Fibonacci | Python | 25.928 | 31.100 | 2.223 | 7.8% | 5/5 |
| Recursive Fibonacci | Node.js | 2.349 | 2.665 | 0.130 | 5.3% | 5/5 |
| Recursive Fibonacci | C# | 0.772 | 0.930 | 0.064 | 7.6% | 5/5 |
| Ackermann function | AquariusLang | 0.532 | 0.700 | 0.068 | 11.8% | 5/5 |
| Ackermann function | AquariusLang (typed) | 0.558 | 0.568 | 0.004 | 0.7% | 5/5 |
| Ackermann function | Python | 10.732 | 13.023 | 1.047 | 9.0% | 5/5 |
| Ackermann function | Node.js | 0.622 | 0.721 | 0.042 | 6.2% | 5/5 |
| Ackermann function | C# | 0.226 | 0.244 | 0.008 | 3.3% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 0.065 | 0.079 | 0.005 | 7.2% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.035 | 0.039 | 0.002 | 5.5% | 5/5 |
| Sieve of Eratosthenes | Python | 0.534 | 0.682 | 0.059 | 10.2% | 5/5 |
| Sieve of Eratosthenes | Node.js | 0.515 | 0.625 | 0.043 | 7.5% | 5/5 |
| Sieve of Eratosthenes | C# | 0.377 | 0.415 | 0.015 | 3.9% | 5/5 |
| Quicksort | AquariusLang | 0.246 | 0.268 | 0.008 | 3.3% | 5/5 |
| Quicksort | AquariusLang (typed) | 0.124 | 0.135 | 0.005 | 3.7% | 5/5 |
| Quicksort | Python | 1.242 | 1.568 | 0.122 | 9.0% | 5/5 |
| Quicksort | Node.js | 0.777 | 1.000 | 0.096 | 10.8% | 5/5 |
| Quicksort | C# | 0.543 | 0.575 | 0.015 | 2.7% | 5/5 |
| Matrix multiplication | AquariusLang | 0.211 | 0.288 | 0.032 | 14.0% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 0.124 | 0.169 | 0.018 | 12.8% | 5/5 |
| Matrix multiplication | Python | 5.216 | 6.309 | 0.444 | 8.0% | 5/5 |
| Matrix multiplication | Node.js | 1.323 | 1.627 | 0.125 | 8.6% | 5/5 |
| Matrix multiplication | C# | 0.273 | 0.372 | 0.039 | 12.7% | 5/5 |
| Mandelbrot set | AquariusLang | 0.288 | 0.398 | 0.041 | 12.4% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 0.296 | 0.371 | 0.029 | 8.8% | 5/5 |
| Mandelbrot set | Python | 9.706 | 15.973 | 2.846 | 24.0% | 5/5 |
| Mandelbrot set | Node.js | 0.947 | 1.259 | 0.120 | 11.3% | 5/5 |
| Mandelbrot set | C# | 0.381 | 0.447 | 0.029 | 7.1% | 5/5 |
| N-Queens | AquariusLang | 0.224 | 0.234 | 0.004 | 1.9% | 5/5 |
| N-Queens | AquariusLang (typed) | 0.196 | 0.211 | 0.006 | 2.7% | 5/5 |
| N-Queens | Python | 3.421 | 4.096 | 0.287 | 7.7% | 5/5 |
| N-Queens | Node.js | 0.672 | 1.095 | 0.182 | 23.7% | 5/5 |
| N-Queens | C# | 0.365 | 0.421 | 0.021 | 5.4% | 5/5 |
| Binary trees | AquariusLang | 1.918 | 2.270 | 0.139 | 6.8% | 5/5 |
| Binary trees | AquariusLang (typed) | 1.993 | 3.324 | 0.648 | 26.1% | 5/5 |
| Binary trees | Python | 8.539 | 10.611 | 0.921 | 9.7% | 5/5 |
| Binary trees | Node.js | 2.623 | 3.164 | 0.242 | 8.3% | 5/5 |
| Binary trees | C# | 1.397 | 1.494 | 0.036 | 2.5% | 5/5 |
| Spectral norm | AquariusLang | 0.273 | 0.298 | 0.010 | 3.7% | 5/5 |
| Spectral norm | AquariusLang (typed) | 0.239 | 0.326 | 0.033 | 12.2% | 5/5 |
| Spectral norm | Python | 14.244 | 22.497 | 3.787 | 20.7% | 5/5 |
| Spectral norm | Node.js | 1.354 | 1.962 | 0.241 | 14.0% | 5/5 |
| Spectral norm | C# | 1.110 | 1.220 | 0.042 | 3.5% | 5/5 |
| Collatz conjecture | AquariusLang | 1.191 | 1.382 | 0.075 | 5.9% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 1.179 | 1.300 | 0.046 | 3.7% | 5/5 |
| Collatz conjecture | Python | 49.710 | 65.862 | 6.743 | 12.5% | 5/5 |
| Collatz conjecture | Node.js | 4.934 | 5.232 | 0.149 | 2.9% | 5/5 |
| Collatz conjecture | C# | 1.355 | 1.466 | 0.040 | 2.8% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 50.50, AquariusLang 39.48, Node.js 39.08, Python 2.26 (higher is faster).**

Pairwise composite speed: C# is 1.98× as fast as AquariusLang (typed); C# is 2.53× as fast as AquariusLang; C# is 2.56× as fast as Node.js; C# is 44.28× as fast as Python; AquariusLang (typed) is 1.28× as fast as AquariusLang; AquariusLang (typed) is 1.29× as fast as Node.js; AquariusLang (typed) is 22.36× as fast as Python; AquariusLang is 1.01× as fast as Node.js; AquariusLang is 17.48× as fast as Python; Node.js is 17.30× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.980× | 2.533× | 2.559× | 44.281× |
| 2 | AquariusLang (typed) | 50.50 | 0.505× | 1.000× | 1.279× | 1.292× | 22.360× |
| 3 | AquariusLang | 39.48 | 0.395× | 0.782× | 1.000× | 1.010× | 17.482× |
| 4 | Node.js | 39.08 | 0.391× | 0.774× | 0.990× | 1.000× | 17.304× |
| 5 | Python | 2.26 | 0.023× | 0.045× | 0.057× | 0.058× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 28 | 1.800 | 1.600 | 26.688 | 2.152 | 0.807 | 0.07× | 0.06× | 0.08× | 0.03× |
| Ackermann function | 6 | 0.572 | 0.567 | 11.702 | 0.369 | 0.127 | 0.05× | 0.05× | 0.03× | 0.01× |
| Sieve of Eratosthenes | 10000 | 0.076 | 0.036 | 0.868 | 0.177 | 0.021 | 0.09× | 0.04× | 0.20× | 0.02× |
| Quicksort | 2000 | 0.226 | 0.113 | 1.388 | 0.169 | 0.073 | 0.16× | 0.08× | 0.12× | 0.05× |
| Matrix multiplication | 45 | 0.201 | 0.121 | 5.501 | 0.291 | 0.056 | 0.04× | 0.02× | 0.05× | 0.01× |
| Mandelbrot set | 80 | 0.294 | 0.307 | 10.152 | 0.248 | 0.230 | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 8 | 0.216 | 0.184 | 3.667 | 0.169 | 0.110 | 0.06× | 0.05× | 0.05× | 0.03× |
| Binary trees | 12 | 2.325 | 1.943 | 8.380 | 0.857 | 0.450 | 0.28× | 0.23× | 0.10× | 0.05× |
| Spectral norm | 60 | 0.273 | 0.248 | 14.700 | 0.240 | 0.128 | 0.02× | 0.02× | 0.02× | 0.01× |
| Collatz conjecture | 10000 | 1.246 | 1.268 | 50.230 | 3.331 | 1.302 | 0.02× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 28 | 1.600 | 2.152 | 1.34× | AquariusLang (typed), 1.34× faster |
| Ackermann function | 6 | 0.567 | 0.369 | 0.65× | Node.js, 1.54× faster |
| Sieve of Eratosthenes | 10000 | 0.036 | 0.177 | 4.97× | AquariusLang (typed), 4.97× faster |
| Quicksort | 2000 | 0.113 | 0.169 | 1.49× | AquariusLang (typed), 1.49× faster |
| Matrix multiplication | 45 | 0.121 | 0.291 | 2.41× | AquariusLang (typed), 2.41× faster |
| Mandelbrot set | 80 | 0.307 | 0.248 | 0.81× | Node.js, 1.24× faster |
| N-Queens | 8 | 0.184 | 0.169 | 0.92× | Node.js, 1.09× faster |
| Binary trees | 12 | 1.943 | 0.857 | 0.44× | Node.js, 2.27× faster |
| Spectral norm | 60 | 0.248 | 0.240 | 0.97× | Node.js, 1.03× faster |
| Collatz conjecture | 10000 | 1.268 | 3.331 | 2.63× | AquariusLang (typed), 2.63× faster |
| **Geometric mean** | | | | **1.29×** | AquariusLang (typed), 1.29× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 1.668 | 1.977 | 0.116 | 6.4% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 1.530 | 7.502 | 2.575 | 86.2% | 5/5 |
| Recursive Fibonacci | Python | 26.593 | 29.143 | 1.107 | 4.0% | 5/5 |
| Recursive Fibonacci | Node.js | 2.072 | 2.493 | 0.189 | 8.4% | 5/5 |
| Recursive Fibonacci | C# | 0.719 | 0.862 | 0.060 | 7.6% | 5/5 |
| Ackermann function | AquariusLang | 0.521 | 0.683 | 0.071 | 12.0% | 5/5 |
| Ackermann function | AquariusLang (typed) | 0.533 | 0.635 | 0.039 | 6.8% | 5/5 |
| Ackermann function | Python | 10.711 | 20.284 | 4.038 | 30.7% | 5/5 |
| Ackermann function | Node.js | 0.352 | 0.539 | 0.079 | 19.9% | 5/5 |
| Ackermann function | C# | 0.120 | 0.127 | 0.004 | 2.9% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 0.072 | 0.076 | 0.002 | 3.0% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.035 | 0.052 | 0.007 | 18.9% | 5/5 |
| Sieve of Eratosthenes | Python | 0.539 | 1.483 | 0.365 | 37.6% | 5/5 |
| Sieve of Eratosthenes | Node.js | 0.121 | 0.222 | 0.042 | 25.6% | 5/5 |
| Sieve of Eratosthenes | C# | 0.017 | 0.025 | 0.003 | 13.0% | 5/5 |
| Quicksort | AquariusLang | 0.212 | 0.250 | 0.014 | 6.0% | 5/5 |
| Quicksort | AquariusLang (typed) | 0.108 | 0.115 | 0.003 | 3.0% | 5/5 |
| Quicksort | Python | 1.359 | 1.518 | 0.081 | 5.7% | 5/5 |
| Quicksort | Node.js | 0.148 | 0.180 | 0.014 | 8.2% | 5/5 |
| Quicksort | C# | 0.069 | 0.084 | 0.006 | 8.0% | 5/5 |
| Matrix multiplication | AquariusLang | 0.174 | 0.222 | 0.021 | 10.5% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 0.118 | 0.132 | 0.006 | 5.2% | 5/5 |
| Matrix multiplication | Python | 5.314 | 6.103 | 0.317 | 5.6% | 5/5 |
| Matrix multiplication | Node.js | 0.124 | 0.358 | 0.087 | 32.3% | 5/5 |
| Matrix multiplication | C# | 0.052 | 0.056 | 0.002 | 3.5% | 5/5 |
| Mandelbrot set | AquariusLang | 0.286 | 0.304 | 0.007 | 2.3% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 0.290 | 0.357 | 0.026 | 8.1% | 5/5 |
| Mandelbrot set | Python | 10.024 | 11.480 | 0.709 | 6.7% | 5/5 |
| Mandelbrot set | Node.js | 0.238 | 0.305 | 0.028 | 10.7% | 5/5 |
| Mandelbrot set | C# | 0.217 | 0.287 | 0.027 | 11.4% | 5/5 |
| N-Queens | AquariusLang | 0.202 | 0.221 | 0.007 | 3.4% | 5/5 |
| N-Queens | AquariusLang (typed) | 0.179 | 0.194 | 0.006 | 3.3% | 5/5 |
| N-Queens | Python | 3.619 | 4.314 | 0.300 | 7.9% | 5/5 |
| N-Queens | Node.js | 0.156 | 0.173 | 0.007 | 4.3% | 5/5 |
| N-Queens | C# | 0.106 | 0.114 | 0.003 | 2.7% | 5/5 |
| Binary trees | AquariusLang | 2.184 | 2.510 | 0.140 | 5.9% | 5/5 |
| Binary trees | AquariusLang (typed) | 1.806 | 2.275 | 0.232 | 11.4% | 5/5 |
| Binary trees | Python | 7.928 | 12.227 | 1.781 | 19.6% | 5/5 |
| Binary trees | Node.js | 0.717 | 1.254 | 0.212 | 23.7% | 5/5 |
| Binary trees | C# | 0.439 | 0.473 | 0.015 | 3.3% | 5/5 |
| Spectral norm | AquariusLang | 0.267 | 0.313 | 0.020 | 7.0% | 5/5 |
| Spectral norm | AquariusLang (typed) | 0.237 | 0.261 | 0.009 | 3.8% | 5/5 |
| Spectral norm | Python | 14.596 | 16.305 | 0.732 | 4.9% | 5/5 |
| Spectral norm | Node.js | 0.235 | 0.248 | 0.005 | 2.1% | 5/5 |
| Spectral norm | C# | 0.122 | 0.143 | 0.008 | 6.4% | 5/5 |
| Collatz conjecture | AquariusLang | 1.176 | 1.769 | 0.241 | 18.0% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 1.258 | 1.698 | 0.191 | 14.0% | 5/5 |
| Collatz conjecture | Python | 47.500 | 56.144 | 3.395 | 6.7% | 5/5 |
| Collatz conjecture | Node.js | 3.180 | 3.438 | 0.128 | 3.9% | 5/5 |
| Collatz conjecture | C# | 1.272 | 1.350 | 0.032 | 2.5% | 5/5 |

## How the composite score is computed

For each mode, the relative speeds on this run's 10 algorithms are combined with equal weights as a geometric mean, and the fastest language is set to 100. Timing uses each language's in-process monotonic timer and covers data initialization and the algorithm and checksum, excluding process start, source or Wasm loading and initial compilation, and output.

Relative speed G = geometric mean (Python median time ÷ the language's median time, per benchmark); composite score = 100 × G ÷ the largest G among all 5 languages, so the top score is always 100. Every algorithm has the same weight; a mode gets composite scores only when all 5 languages pass every selected test in that mode. Scores from different modes, test sets or input sizes cannot be compared directly.

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
- All 5 languages start timing after the function definitions and before data initialization, and stop after the algorithm and checksum, before output. Memory allocation, garbage collection and on-demand JIT during the run still count. `elapsed_ms` in the JSON and CSV is the process value (the median of the in-process timed runs; `run_elapsed_ms` keeps each run); `process_elapsed_ms` also keeps the whole-process time for diagnosis and takes no part in the statistics or ranking.
- Standard mode: Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.
- Warmed mode: Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.
- Each script wraps the timed work in a `benchmark_run` function; in-process warm-up only calls that function more often and changes neither the algorithm nor the timed interval.
- AquariusLang always builds the Wasm with `aqua build` before measuring, then runs `aqua run`; Wasm generation is not part of the sample time, and each mode's copy is built separately. "AquariusLang (typed)" uses the same compiler and the same algorithms, adding only optional type annotations on variables, parameters and return values (`benchmarks/aquarius_typed/`); typed functions must declare a return type, so the in-place functions of quicksort and spectral norm gain a `回傳 0;` (`return 0;`) line, and binary trees annotate the tree arrays as `陣列` (`Array`, an array whose elements can be any value). Python runs the source, and Node.js uses V8. C# is compiled ahead of time into a net8.0 assembly with `dotnet build --configuration Release` and run directly as `dotnet Benchmark.dll`; build and restore are not timed, and no external NuGet packages are used. The initial JIT before Main is not timed; on-demand JIT inside the timed interval still counts. The assembly turns tiered compilation off (`TieredCompilation=false`), so each method is compiled by the optimizing JIT on its first call, matching the optimized Wasmtime compilation AquariusLang finishes before timing. No NumPy, native algorithm libraries, worker threads or built-in sorts are used.
- Warm-up process samples are discarded; they warm the operating system's file cache, and no JIT or VM state carries over between processes. Each round shuffles every algorithm, language and mode combination with the recorded random seed, then runs them in that order.
- Every timed run of every warm-up and counted sample must match the untimed Python reference answer. Integers must be identical; the squared spectral norm allows a relative error of 1e-9 and an absolute error of 1e-12. A non-zero exit code, a timeout, missing or extra standard output, a non-finite value or a checksum mismatch fails the test. The timing output must be a finite millisecond value above zero; a missing timing does not fall back to whole-process timing.
- AquariusLang's integer `/` truncates; Python uses `//` and Node.js `Math.trunc` to match. Floating-point tests use double precision (AquariusLang uses `d` literals); at the standard size every intermediate integer stays within the signed 32-bit range.
- Array construction has the same linear cost in every language: AquariusLang preallocates with `陣列.建立` (`Array.Make`; quicksort uses `陣列.追加`, `Array.Append`, with reserved capacity), Python uses `[value] * n` / `append`, Node.js `push`, C# `new T[n]` (with `Array.Fill` where needed); no append that copies the whole array each time is used.
- Compilation timing: Wasmtime has fully compiled the AquariusLang Wasm to machine code before timing starts. C# has tiered compilation off, so methods are compiled by the optimizing JIT on their first call; in standard mode that JIT is still inside the timed interval. Node.js (V8) cannot optimize ahead of time and starts in its interpreter and baseline compiler; in standard mode hot functions are optimized inside the timed interval, which favors AquariusLang; warmed mode relies on in-process warm-up to optimize hot functions before timing, though a little JIT or garbage collection may still fall inside the timed interval. At the standard size each test takes about 1 millisecond, so timer and allocation noise weigh more; `--profile large` reduces this with larger inputs, and the scores of the two sizes must not be mixed.
- Small workloads can be affected by timer and function call costs; warmed mode warms up only a few times and is not the steady-state speed of a long run, while standard mode reflects only the first run; neither represents a language ranking for every program. CPU frequency, temperature, background work and scheduling noise are not controlled. Process memory use and CPU time are not measured; the RAM below is the machine's installed memory.

## Test date and environment

- Started: 2026-10-29T03:32:11.555006+08:00
- Finished: 2026-10-29T03:34:37.286744+08:00
- Time zone: Asia/Taipei
- Input size: standard (`standard`); 5 counted and 1 discarded warm-up processes per case
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
| AquariusLang | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua\aqua.exe |
| AquariusLang (typed) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua\aqua.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.exe |
| C# | SDKs: 8.0.426 [C:\Program Files\dotnet\sdk] Runtimes: Microsoft.AspNetCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App] Microsoft.NETCore.App 6.0.36 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.WindowsDesktop.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] Microsoft.WindowsDesktop.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] | C:\Program Files\dotnet\dotnet.exe |

AquariusLang release folder: `C:\OfficialProjects\AquariusLangTW\dist\aqua`.

AquariusLang launcher SHA-256: `9c8bee82ed9c872ab2b0e055b90a4ecf50de4c1be8a34135459329f3736b2712`.


## Correctness

Every warm-up and counted sample output, in every language and mode, matches the Python reference answer.

| Benchmark | Expected result | Workload |
| --- | ---: | --- |
| Recursive Fibonacci | 317811 | Naive recursion, no memoization. |
| Ackermann function | 509 | Computes A(3, n), exercising nested recursive calls. |
| Sieve of Eratosthenes | 1229 | Counts the primes from 2 to n (inclusive) with a Boolean array. |
| Quicksort | 616973 | Sorts a fixed-seed linear congruential sequence in place with the middle element as pivot; checks the order and a weighted checksum. |
| Matrix multiplication | 545940 | Row-major one-dimensional arrays and an i/j/k triple loop; sums every element of the result matrix. |
| Mandelbrot set | 129059 | Samples n × n points over [-2, 1) × [-1, 1) with at most 60 iterations and sums the escape iteration counts. |
| N-Queens | 92 | Counts every solution by backtracking, checking columns and diagonals. |
| Binary trees | 65528 | Builds eight complete binary trees of depth n and counts their nodes recursively. |
| Spectral norm | 1.6236011690579917 | Runs ten power iterations on an implicit matrix and prints the squared spectral norm, avoiding a library square root. |
| Collatz conjecture | 849666 | Sums the steps for each start from 1 to n to reach 1, no memoization. |

## Reproducible data

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261029-033211-555006\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261029-033211-555006\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261029-033211-555006\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

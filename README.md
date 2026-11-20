# Desktop performance benchmark: AquariusLang, AquariusLang (typed), AquariusLang (Native AOT compiler), AquariusLang (typed, Native AOT compiler), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: C# 100.00, AquariusLang (typed, Native AOT compiler) 67.81, AquariusLang (typed) 66.28, AquariusLang 50.62, AquariusLang (Native AOT compiler) 49.45, Node.js 38.72, Python 2.80
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 56.79, AquariusLang (typed, Native AOT compiler) 56.65, Node.js 46.98, AquariusLang 45.17, AquariusLang (Native AOT compiler) 43.81, Python 2.27

The project provides ten classic algorithms, 70 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports. The app suite (hashes, strings, closures, structs and calls, the operations everyday programs use) is in [app/README.md](app/README.md).

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: C# 100.00, AquariusLang (typed, Native AOT compiler) 67.81, AquariusLang (typed) 66.28, AquariusLang 50.62, AquariusLang (Native AOT compiler) 49.45, Node.js 38.72, Python 2.80 (higher is faster).**

Pairwise composite speed: C# is 1.47× as fast as AquariusLang (typed, Native AOT compiler); C# is 1.51× as fast as AquariusLang (typed); C# is 1.98× as fast as AquariusLang; C# is 2.02× as fast as AquariusLang (Native AOT compiler); C# is 2.58× as fast as Node.js; C# is 35.73× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.02× as fast as AquariusLang (typed); AquariusLang (typed, Native AOT compiler) is 1.34× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 1.37× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 1.75× as fast as Node.js; AquariusLang (typed, Native AOT compiler) is 24.23× as fast as Python; AquariusLang (typed) is 1.31× as fast as AquariusLang; AquariusLang (typed) is 1.34× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 1.71× as fast as Node.js; AquariusLang (typed) is 23.68× as fast as Python; AquariusLang is 1.02× as fast as AquariusLang (Native AOT compiler); AquariusLang is 1.31× as fast as Node.js; AquariusLang is 18.08× as fast as Python; AquariusLang (Native AOT compiler) is 1.28× as fast as Node.js; AquariusLang (Native AOT compiler) is 17.67× as fast as Python; Node.js is 13.84× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs AquariusLang (Native AOT compiler) | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.475× | 1.509× | 1.976× | 2.022× | 2.582× | 35.727× |
| 2 | AquariusLang (typed, Native AOT compiler) | 67.81 | 0.678× | 1.000× | 1.023× | 1.340× | 1.371× | 1.751× | 24.228× |
| 3 | AquariusLang (typed) | 66.28 | 0.663× | 0.977× | 1.000× | 1.309× | 1.340× | 1.712× | 23.679× |
| 4 | AquariusLang | 50.62 | 0.506× | 0.746× | 0.764× | 1.000× | 1.024× | 1.307× | 18.083× |
| 5 | AquariusLang (Native AOT compiler) | 49.45 | 0.495× | 0.729× | 0.746× | 0.977× | 1.000× | 1.277× | 17.668× |
| 6 | Node.js | 38.72 | 0.387× | 0.571× | 0.584× | 0.765× | 0.783× | 1.000× | 13.835× |
| 7 | Python | 2.80 | 0.028× | 0.041× | 0.042× | 0.055× | 0.057× | 0.072× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 13.097 | 14.529 | 14.080 | 14.203 | 227.480 | 16.122 | 7.035 | 0.06× | 0.06× | 0.06× | 0.06× | 0.07× | 0.03× |
| Ackermann function | 8 | 11.830 | 10.120 | 11.282 | 10.670 | 255.947 | 9.281 | 3.028 | 0.05× | 0.04× | 0.04× | 0.04× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.997 | 1.204 | 2.006 | 0.964 | 16.948 | 6.959 | 1.002 | 0.12× | 0.07× | 0.12× | 0.06× | 0.41× | 0.06× |
| Quicksort | 30000 | 6.041 | 3.016 | 6.317 | 3.035 | 34.556 | 7.624 | 2.744 | 0.17× | 0.09× | 0.18× | 0.09× | 0.22× | 0.08× |
| Matrix multiplication | 150 | 8.005 | 2.656 | 8.462 | 2.812 | 263.462 | 10.056 | 2.663 | 0.03× | 0.01× | 0.03× | 0.01× | 0.04× | 0.01× |
| Mandelbrot set | 300 | 5.533 | 6.254 | 5.637 | 5.514 | 185.413 | 5.613 | 4.225 | 0.03× | 0.03× | 0.03× | 0.03× | 0.03× | 0.02× |
| N-Queens | 10 | 6.978 | 5.620 | 7.363 | 5.490 | 119.824 | 5.923 | 4.243 | 0.06× | 0.05× | 0.06× | 0.05× | 0.05× | 0.04× |
| Binary trees | 16 | 69.036 | 62.243 | 67.338 | 66.435 | 425.454 | 33.175 | 21.431 | 0.16× | 0.15× | 0.16× | 0.16× | 0.08× | 0.05× |
| Spectral norm | 250 | 6.536 | 4.844 | 6.577 | 4.850 | 335.411 | 14.591 | 4.271 | 0.02× | 0.01× | 0.02× | 0.01× | 0.04× | 0.01× |
| Collatz conjecture | 100000 | 21.006 | 24.575 | 22.063 | 24.173 | 718.901 | 62.042 | 23.609 | 0.03× | 0.03× | 0.03× | 0.03× | 0.09× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 14.529 | 16.122 | 1.11× | AquariusLang (typed), 1.11× faster |
| Ackermann function | 8 | 10.120 | 9.281 | 0.92× | Node.js, 1.09× faster |
| Sieve of Eratosthenes | 200000 | 1.204 | 6.959 | 5.78× | AquariusLang (typed), 5.78× faster |
| Quicksort | 30000 | 3.016 | 7.624 | 2.53× | AquariusLang (typed), 2.53× faster |
| Matrix multiplication | 150 | 2.656 | 10.056 | 3.79× | AquariusLang (typed), 3.79× faster |
| Mandelbrot set | 300 | 6.254 | 5.613 | 0.90× | Node.js, 1.11× faster |
| N-Queens | 10 | 5.620 | 5.923 | 1.05× | AquariusLang (typed), 1.05× faster |
| Binary trees | 16 | 62.243 | 33.175 | 0.53× | Node.js, 1.88× faster |
| Spectral norm | 250 | 4.844 | 14.591 | 3.01× | AquariusLang (typed), 3.01× faster |
| Collatz conjecture | 100000 | 24.575 | 62.042 | 2.52× | AquariusLang (typed), 2.52× faster |
| **Geometric mean** | | | | **1.71×** | AquariusLang (typed), 1.71× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 10.021 | 15.460 | 2.176 | 16.3% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 12.223 | 16.570 | 1.620 | 11.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (Native AOT compiler) | 11.666 | 15.586 | 1.507 | 11.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed, Native AOT compiler) | 12.758 | 16.393 | 1.447 | 9.9% | 5/5 |
| Recursive Fibonacci | Python | 184.864 | 236.526 | 21.087 | 9.7% | 5/5 |
| Recursive Fibonacci | Node.js | 12.882 | 17.814 | 2.249 | 14.5% | 5/5 |
| Recursive Fibonacci | C# | 5.619 | 7.329 | 0.683 | 10.1% | 5/5 |
| Ackermann function | AquariusLang | 11.020 | 12.924 | 0.759 | 6.4% | 5/5 |
| Ackermann function | AquariusLang (typed) | 8.964 | 11.571 | 0.952 | 9.3% | 5/5 |
| Ackermann function | AquariusLang (Native AOT compiler) | 8.051 | 12.451 | 1.778 | 16.6% | 5/5 |
| Ackermann function | AquariusLang (typed, Native AOT compiler) | 10.117 | 11.929 | 0.691 | 6.4% | 5/5 |
| Ackermann function | Python | 194.142 | 343.417 | 65.990 | 25.2% | 5/5 |
| Ackermann function | Node.js | 7.396 | 10.477 | 1.231 | 13.2% | 5/5 |
| Ackermann function | C# | 2.120 | 5.232 | 1.168 | 34.1% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.901 | 2.155 | 0.103 | 5.1% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.857 | 1.327 | 0.180 | 15.5% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (Native AOT compiler) | 1.982 | 2.216 | 0.103 | 5.0% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed, Native AOT compiler) | 0.847 | 1.285 | 0.177 | 17.5% | 5/5 |
| Sieve of Eratosthenes | Python | 13.945 | 18.860 | 1.768 | 10.6% | 5/5 |
| Sieve of Eratosthenes | Node.js | 5.229 | 8.092 | 1.024 | 15.0% | 5/5 |
| Sieve of Eratosthenes | C# | 0.791 | 1.078 | 0.115 | 11.7% | 5/5 |
| Quicksort | AquariusLang | 4.314 | 7.053 | 1.102 | 18.3% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.624 | 3.653 | 0.381 | 12.2% | 5/5 |
| Quicksort | AquariusLang (Native AOT compiler) | 5.485 | 7.222 | 0.723 | 11.5% | 5/5 |
| Quicksort | AquariusLang (typed, Native AOT compiler) | 2.860 | 3.460 | 0.254 | 8.2% | 5/5 |
| Quicksort | Python | 29.836 | 36.984 | 2.825 | 8.2% | 5/5 |
| Quicksort | Node.js | 6.004 | 8.154 | 0.825 | 11.2% | 5/5 |
| Quicksort | C# | 2.047 | 3.782 | 0.753 | 26.8% | 5/5 |
| Matrix multiplication | AquariusLang | 7.321 | 8.631 | 0.579 | 7.2% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.028 | 3.040 | 0.432 | 16.9% | 5/5 |
| Matrix multiplication | AquariusLang (Native AOT compiler) | 6.709 | 9.547 | 1.224 | 15.0% | 5/5 |
| Matrix multiplication | AquariusLang (typed, Native AOT compiler) | 2.208 | 3.135 | 0.396 | 14.8% | 5/5 |
| Matrix multiplication | Python | 221.908 | 289.668 | 27.584 | 10.6% | 5/5 |
| Matrix multiplication | Node.js | 8.321 | 11.345 | 1.416 | 14.3% | 5/5 |
| Matrix multiplication | C# | 1.944 | 3.332 | 0.589 | 23.2% | 5/5 |
| Mandelbrot set | AquariusLang | 4.293 | 6.079 | 0.672 | 12.5% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 5.566 | 7.185 | 0.581 | 9.2% | 5/5 |
| Mandelbrot set | AquariusLang (Native AOT compiler) | 4.187 | 5.836 | 0.827 | 16.1% | 5/5 |
| Mandelbrot set | AquariusLang (typed, Native AOT compiler) | 4.129 | 6.993 | 1.218 | 22.7% | 5/5 |
| Mandelbrot set | Python | 176.751 | 190.623 | 5.295 | 2.9% | 5/5 |
| Mandelbrot set | Node.js | 4.914 | 6.874 | 0.870 | 15.2% | 5/5 |
| Mandelbrot set | C# | 3.298 | 4.670 | 0.555 | 13.5% | 5/5 |
| N-Queens | AquariusLang | 5.489 | 7.650 | 1.043 | 15.7% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.873 | 5.892 | 0.420 | 7.6% | 5/5 |
| N-Queens | AquariusLang (Native AOT compiler) | 5.479 | 7.469 | 0.879 | 12.9% | 5/5 |
| N-Queens | AquariusLang (typed, Native AOT compiler) | 3.961 | 6.115 | 0.817 | 15.4% | 5/5 |
| N-Queens | Python | 96.196 | 153.358 | 21.464 | 17.8% | 5/5 |
| N-Queens | Node.js | 4.322 | 6.329 | 0.776 | 13.8% | 5/5 |
| N-Queens | C# | 3.275 | 4.961 | 0.796 | 19.1% | 5/5 |
| Binary trees | AquariusLang | 47.148 | 73.377 | 12.457 | 20.3% | 5/5 |
| Binary trees | AquariusLang (typed) | 51.144 | 70.981 | 8.329 | 13.8% | 5/5 |
| Binary trees | AquariusLang (Native AOT compiler) | 48.284 | 70.464 | 9.151 | 14.3% | 5/5 |
| Binary trees | AquariusLang (typed, Native AOT compiler) | 53.511 | 70.561 | 7.769 | 12.3% | 5/5 |
| Binary trees | Python | 270.448 | 477.428 | 97.227 | 25.6% | 5/5 |
| Binary trees | Node.js | 27.022 | 38.288 | 5.189 | 15.7% | 5/5 |
| Binary trees | C# | 18.503 | 24.477 | 2.227 | 10.4% | 5/5 |
| Spectral norm | AquariusLang | 6.119 | 6.716 | 0.252 | 3.9% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.576 | 5.636 | 0.789 | 16.5% | 5/5 |
| Spectral norm | AquariusLang (Native AOT compiler) | 6.123 | 8.136 | 0.822 | 12.1% | 5/5 |
| Spectral norm | AquariusLang (typed, Native AOT compiler) | 3.745 | 5.262 | 0.568 | 12.2% | 5/5 |
| Spectral norm | Python | 287.006 | 358.178 | 26.228 | 8.0% | 5/5 |
| Spectral norm | Node.js | 8.624 | 24.916 | 5.989 | 39.2% | 5/5 |
| Spectral norm | C# | 3.088 | 4.391 | 0.558 | 14.0% | 5/5 |
| Collatz conjecture | AquariusLang | 15.779 | 22.224 | 2.522 | 12.5% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.671 | 28.439 | 3.949 | 16.4% | 5/5 |
| Collatz conjecture | AquariusLang (Native AOT compiler) | 16.483 | 23.105 | 2.915 | 14.3% | 5/5 |
| Collatz conjecture | AquariusLang (typed, Native AOT compiler) | 23.080 | 28.714 | 2.419 | 9.6% | 5/5 |
| Collatz conjecture | Python | 636.191 | 808.346 | 82.615 | 11.5% | 5/5 |
| Collatz conjecture | Node.js | 46.198 | 63.851 | 7.339 | 12.6% | 5/5 |
| Collatz conjecture | C# | 17.694 | 25.766 | 3.865 | 17.7% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 56.79, AquariusLang (typed, Native AOT compiler) 56.65, Node.js 46.98, AquariusLang 45.17, AquariusLang (Native AOT compiler) 43.81, Python 2.27 (higher is faster).**

Pairwise composite speed: C# is 1.76× as fast as AquariusLang (typed); C# is 1.77× as fast as AquariusLang (typed, Native AOT compiler); C# is 2.13× as fast as Node.js; C# is 2.21× as fast as AquariusLang; C# is 2.28× as fast as AquariusLang (Native AOT compiler); C# is 43.96× as fast as Python; AquariusLang (typed) is 1.00× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (typed) is 1.21× as fast as Node.js; AquariusLang (typed) is 1.26× as fast as AquariusLang; AquariusLang (typed) is 1.30× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 24.96× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.21× as fast as Node.js; AquariusLang (typed, Native AOT compiler) is 1.25× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 1.29× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 24.90× as fast as Python; Node.js is 1.04× as fast as AquariusLang; Node.js is 1.07× as fast as AquariusLang (Native AOT compiler); Node.js is 20.65× as fast as Python; AquariusLang is 1.03× as fast as AquariusLang (Native AOT compiler); AquariusLang is 19.85× as fast as Python; AquariusLang (Native AOT compiler) is 19.26× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs Node.js | Speed vs AquariusLang | Speed vs AquariusLang (Native AOT compiler) | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.761× | 1.765× | 2.128× | 2.214× | 2.283× | 43.957× |
| 2 | AquariusLang (typed) | 56.79 | 0.568× | 1.000× | 1.003× | 1.209× | 1.257× | 1.296× | 24.962× |
| 3 | AquariusLang (typed, Native AOT compiler) | 56.65 | 0.566× | 0.997× | 1.000× | 1.206× | 1.254× | 1.293× | 24.900× |
| 4 | Node.js | 46.98 | 0.470× | 0.827× | 0.829× | 1.000× | 1.040× | 1.072× | 20.653× |
| 5 | AquariusLang | 45.17 | 0.452× | 0.795× | 0.797× | 0.961× | 1.000× | 1.031× | 19.854× |
| 6 | AquariusLang (Native AOT compiler) | 43.81 | 0.438× | 0.771× | 0.773× | 0.932× | 0.970× | 1.000× | 19.258× |
| 7 | Python | 2.27 | 0.023× | 0.040× | 0.040× | 0.048× | 0.050× | 0.052× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 13.329 | 13.749 | 13.345 | 12.841 | 228.988 | 16.680 | 5.911 | 0.06× | 0.06× | 0.06× | 0.06× | 0.07× | 0.03× |
| Ackermann function | 8 | 10.648 | 9.247 | 10.457 | 10.087 | 257.438 | 8.962 | 2.905 | 0.04× | 0.04× | 0.04× | 0.04× | 0.03× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.443 | 1.019 | 1.543 | 1.042 | 15.346 | 2.829 | 0.472 | 0.09× | 0.07× | 0.10× | 0.07× | 0.18× | 0.03× |
| Quicksort | 30000 | 5.646 | 3.018 | 5.619 | 2.951 | 33.111 | 3.793 | 2.016 | 0.17× | 0.09× | 0.17× | 0.09× | 0.11× | 0.06× |
| Matrix multiplication | 150 | 8.095 | 2.909 | 7.898 | 2.899 | 268.273 | 6.589 | 2.374 | 0.03× | 0.01× | 0.03× | 0.01× | 0.02× | 0.01× |
| Mandelbrot set | 300 | 5.489 | 5.405 | 5.419 | 5.354 | 180.802 | 3.865 | 4.072 | 0.03× | 0.03× | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 10 | 7.076 | 5.447 | 7.580 | 5.551 | 120.384 | 4.650 | 3.834 | 0.06× | 0.05× | 0.06× | 0.05× | 0.04× | 0.03× |
| Binary trees | 16 | 51.023 | 52.811 | 55.509 | 55.180 | 404.134 | 14.996 | 21.274 | 0.13× | 0.13× | 0.14× | 0.14× | 0.04× | 0.05× |
| Spectral norm | 250 | 5.409 | 5.009 | 5.852 | 4.634 | 335.903 | 8.543 | 2.571 | 0.02× | 0.01× | 0.02× | 0.01× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 19.614 | 22.502 | 20.940 | 23.304 | 788.900 | 54.498 | 21.019 | 0.02× | 0.03× | 0.03× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 13.749 | 16.680 | 1.21× | AquariusLang (typed), 1.21× faster |
| Ackermann function | 8 | 9.247 | 8.962 | 0.97× | Node.js, 1.03× faster |
| Sieve of Eratosthenes | 200000 | 1.019 | 2.829 | 2.78× | AquariusLang (typed), 2.78× faster |
| Quicksort | 30000 | 3.018 | 3.793 | 1.26× | AquariusLang (typed), 1.26× faster |
| Matrix multiplication | 150 | 2.909 | 6.589 | 2.27× | AquariusLang (typed), 2.27× faster |
| Mandelbrot set | 300 | 5.405 | 3.865 | 0.72× | Node.js, 1.40× faster |
| N-Queens | 10 | 5.447 | 4.650 | 0.85× | Node.js, 1.17× faster |
| Binary trees | 16 | 52.811 | 14.996 | 0.28× | Node.js, 3.52× faster |
| Spectral norm | 250 | 5.009 | 8.543 | 1.71× | AquariusLang (typed), 1.71× faster |
| Collatz conjecture | 100000 | 22.502 | 54.498 | 2.42× | AquariusLang (typed), 2.42× faster |
| **Geometric mean** | | | | **1.21×** | AquariusLang (typed), 1.21× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 10.451 | 14.220 | 1.501 | 11.9% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 11.221 | 14.424 | 1.475 | 11.3% | 5/5 |
| Recursive Fibonacci | AquariusLang (Native AOT compiler) | 12.909 | 13.896 | 0.387 | 2.9% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed, Native AOT compiler) | 10.339 | 13.654 | 1.357 | 10.8% | 5/5 |
| Recursive Fibonacci | Python | 196.124 | 243.037 | 21.167 | 9.6% | 5/5 |
| Recursive Fibonacci | Node.js | 14.137 | 17.766 | 1.360 | 8.3% | 5/5 |
| Recursive Fibonacci | C# | 5.171 | 6.908 | 0.713 | 11.8% | 5/5 |
| Ackermann function | AquariusLang | 7.782 | 11.349 | 1.389 | 13.7% | 5/5 |
| Ackermann function | AquariusLang (typed) | 7.282 | 9.869 | 1.026 | 11.4% | 5/5 |
| Ackermann function | AquariusLang (Native AOT compiler) | 9.180 | 11.525 | 0.844 | 8.2% | 5/5 |
| Ackermann function | AquariusLang (typed, Native AOT compiler) | 7.484 | 10.421 | 1.467 | 15.9% | 5/5 |
| Ackermann function | Python | 209.231 | 261.275 | 21.715 | 8.8% | 5/5 |
| Ackermann function | Node.js | 7.344 | 9.561 | 0.837 | 9.6% | 5/5 |
| Ackermann function | C# | 2.247 | 2.981 | 0.320 | 11.8% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.237 | 2.043 | 0.303 | 19.6% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.889 | 1.080 | 0.073 | 7.2% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (Native AOT compiler) | 1.360 | 1.702 | 0.132 | 8.5% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed, Native AOT compiler) | 0.889 | 1.187 | 0.124 | 12.2% | 5/5 |
| Sieve of Eratosthenes | Python | 14.140 | 19.019 | 2.142 | 13.1% | 5/5 |
| Sieve of Eratosthenes | Node.js | 2.203 | 3.097 | 0.409 | 15.1% | 5/5 |
| Sieve of Eratosthenes | C# | 0.378 | 0.539 | 0.061 | 12.8% | 5/5 |
| Quicksort | AquariusLang | 4.900 | 6.701 | 0.798 | 13.9% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.794 | 3.380 | 0.231 | 7.6% | 5/5 |
| Quicksort | AquariusLang (Native AOT compiler) | 4.458 | 6.082 | 0.716 | 13.2% | 5/5 |
| Quicksort | AquariusLang (typed, Native AOT compiler) | 2.507 | 3.271 | 0.293 | 10.2% | 5/5 |
| Quicksort | Python | 26.351 | 36.977 | 4.748 | 14.9% | 5/5 |
| Quicksort | Node.js | 2.949 | 4.122 | 0.436 | 11.9% | 5/5 |
| Quicksort | C# | 1.525 | 2.175 | 0.326 | 17.3% | 5/5 |
| Matrix multiplication | AquariusLang | 6.093 | 14.865 | 3.392 | 37.3% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.288 | 3.041 | 0.325 | 11.9% | 5/5 |
| Matrix multiplication | AquariusLang (Native AOT compiler) | 6.189 | 8.394 | 0.871 | 11.6% | 5/5 |
| Matrix multiplication | AquariusLang (typed, Native AOT compiler) | 2.187 | 3.088 | 0.365 | 13.3% | 5/5 |
| Matrix multiplication | Python | 209.007 | 275.311 | 27.755 | 11.0% | 5/5 |
| Matrix multiplication | Node.js | 3.142 | 7.003 | 1.717 | 30.8% | 5/5 |
| Matrix multiplication | C# | 1.755 | 2.701 | 0.355 | 15.5% | 5/5 |
| Mandelbrot set | AquariusLang | 4.418 | 6.394 | 0.829 | 15.4% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.372 | 5.867 | 0.657 | 12.5% | 5/5 |
| Mandelbrot set | AquariusLang (Native AOT compiler) | 4.642 | 5.950 | 0.502 | 9.2% | 5/5 |
| Mandelbrot set | AquariusLang (typed, Native AOT compiler) | 4.080 | 5.905 | 0.734 | 13.8% | 5/5 |
| Mandelbrot set | Python | 144.489 | 188.078 | 22.520 | 13.3% | 5/5 |
| Mandelbrot set | Node.js | 3.155 | 4.805 | 0.785 | 20.0% | 5/5 |
| Mandelbrot set | C# | 3.023 | 4.326 | 0.529 | 13.6% | 5/5 |
| N-Queens | AquariusLang | 6.052 | 8.065 | 0.767 | 10.7% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.553 | 5.715 | 0.542 | 10.5% | 5/5 |
| N-Queens | AquariusLang (Native AOT compiler) | 5.565 | 7.974 | 1.209 | 17.4% | 5/5 |
| N-Queens | AquariusLang (typed, Native AOT compiler) | 4.230 | 5.920 | 0.660 | 12.3% | 5/5 |
| N-Queens | Python | 99.873 | 132.898 | 15.384 | 13.2% | 5/5 |
| N-Queens | Node.js | 4.032 | 5.298 | 0.474 | 10.2% | 5/5 |
| N-Queens | C# | 3.117 | 3.934 | 0.331 | 9.0% | 5/5 |
| Binary trees | AquariusLang | 40.996 | 61.409 | 7.921 | 15.3% | 5/5 |
| Binary trees | AquariusLang (typed) | 47.745 | 59.657 | 4.305 | 8.0% | 5/5 |
| Binary trees | AquariusLang (Native AOT compiler) | 37.077 | 59.492 | 10.315 | 20.5% | 5/5 |
| Binary trees | AquariusLang (typed, Native AOT compiler) | 49.086 | 58.937 | 4.112 | 7.6% | 5/5 |
| Binary trees | Python | 296.135 | 458.608 | 71.979 | 18.9% | 5/5 |
| Binary trees | Node.js | 13.915 | 17.947 | 1.997 | 12.7% | 5/5 |
| Binary trees | C# | 13.955 | 24.303 | 4.078 | 19.6% | 5/5 |
| Spectral norm | AquariusLang | 4.940 | 5.885 | 0.391 | 7.2% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.988 | 5.334 | 0.523 | 10.9% | 5/5 |
| Spectral norm | AquariusLang (Native AOT compiler) | 4.856 | 6.386 | 0.631 | 10.8% | 5/5 |
| Spectral norm | AquariusLang (typed, Native AOT compiler) | 4.076 | 5.903 | 0.752 | 15.2% | 5/5 |
| Spectral norm | Python | 278.254 | 352.966 | 35.787 | 11.2% | 5/5 |
| Spectral norm | Node.js | 7.117 | 9.473 | 1.088 | 13.1% | 5/5 |
| Spectral norm | C# | 2.070 | 3.187 | 0.482 | 18.7% | 5/5 |
| Collatz conjecture | AquariusLang | 15.620 | 21.830 | 2.790 | 15.0% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.657 | 25.741 | 2.940 | 13.3% | 5/5 |
| Collatz conjecture | AquariusLang (Native AOT compiler) | 15.894 | 23.441 | 2.785 | 13.7% | 5/5 |
| Collatz conjecture | AquariusLang (typed, Native AOT compiler) | 17.887 | 25.872 | 3.190 | 13.9% | 5/5 |
| Collatz conjecture | Python | 633.429 | 849.057 | 80.994 | 10.5% | 5/5 |
| Collatz conjecture | Node.js | 43.397 | 59.281 | 7.488 | 14.5% | 5/5 |
| Collatz conjecture | C# | 17.551 | 25.232 | 3.404 | 16.2% | 5/5 |

## AquariusLang compiler build and start times

Each AquariusLang candidate builds every program with its own `aqua` (`aqua build`) and runs it (`aqua run`). Workload timings exclude both; the table shows the median build time over every benchmark and mode, and per mode the median whole-process time (starting `aqua` and the runtime included).

| Candidate | Median build | Median process, standard mode | Median process, warmed mode |
| --- | ---: | ---: | ---: |
| AquariusLang | 157.6 ms | 146.9 ms | 234.6 ms |
| AquariusLang (typed) | 158.9 ms | 177.2 ms | 216.3 ms |
| AquariusLang (Native AOT compiler) | 35.7 ms | 120.9 ms | 158.3 ms |
| AquariusLang (typed, Native AOT compiler) | 36.2 ms | 96.1 ms | 167.9 ms |

## How the composite score is computed

For each mode, the relative speeds on this run's 10 algorithms are combined with equal weights as a geometric mean, and the fastest language is set to 100. Timing uses each language's in-process monotonic timer and covers data initialization and the algorithm and checksum, excluding process start, source or Wasm loading and initial compilation, and output.

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

- Started: 2026-11-20T17:43:43.993405+08:00
- Finished: 2026-11-20T17:49:59.062170+08:00
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
| Recursive Fibonacci | 2178309 | Naive recursion, no memoization. |
| Ackermann function | 2045 | Computes A(3, n), exercising nested recursive calls. |
| Sieve of Eratosthenes | 17984 | Counts the primes from 2 to n (inclusive) with a Boolean array. |
| Quicksort | 64059 | Sorts a fixed-seed linear congruential sequence in place with the middle element as pivot; checks the order and a weighted checksum. |
| Matrix multiplication | 20247300 | Row-major one-dimensional arrays and an i/j/k triple loop; sums every element of the result matrix. |
| Mandelbrot set | 1796247 | Samples n × n points over [-2, 1) × [-1, 1) with at most 60 iterations and sums the escape iteration counts. |
| N-Queens | 724 | Counts every solution by backtracking, checking columns and diagonals. |
| Binary trees | 1048568 | Builds eight complete binary trees of depth n and counts their nodes recursively. |
| Spectral norm | 1.623646462323075 | Runs ten power iterations on an implicit matrix and prints the squared spectral norm, avoiding a library square root. |
| Collatz conjecture | 10753840 | Sums the steps for each start from 1 to n to reach 1, no memoization. |

## Reproducible data

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261120-174343-993405\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261120-174343-993405\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261120-174343-993405\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/aquarius_aot/`, `benchmarks/aquarius_typed_aot/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

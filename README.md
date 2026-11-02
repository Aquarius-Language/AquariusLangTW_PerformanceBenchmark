# Desktop performance benchmark: AquariusLang, AquariusLang (typed), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: C# 100.00, AquariusLang (typed) 66.50, AquariusLang 49.92, Node.js 36.42, Python 2.58
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 56.10, Node.js 45.77, AquariusLang 43.32, Python 1.87

The project provides ten classic algorithms, 50 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: C# 100.00, AquariusLang (typed) 66.50, AquariusLang 49.92, Node.js 36.42, Python 2.58 (higher is faster).**

Pairwise composite speed: C# is 1.50× as fast as AquariusLang (typed); C# is 2.00× as fast as AquariusLang; C# is 2.75× as fast as Node.js; C# is 38.80× as fast as Python; AquariusLang (typed) is 1.33× as fast as AquariusLang; AquariusLang (typed) is 1.83× as fast as Node.js; AquariusLang (typed) is 25.81× as fast as Python; AquariusLang is 1.37× as fast as Node.js; AquariusLang is 19.37× as fast as Python; Node.js is 14.13× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.504× | 2.003× | 2.746× | 38.804× |
| 2 | AquariusLang (typed) | 66.50 | 0.665× | 1.000× | 1.332× | 1.826× | 25.805× |
| 3 | AquariusLang | 49.92 | 0.499× | 0.751× | 1.000× | 1.371× | 19.369× |
| 4 | Node.js | 36.42 | 0.364× | 0.548× | 0.730× | 1.000× | 14.131× |
| 5 | Python | 2.58 | 0.026× | 0.039× | 0.052× | 0.071× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 11.034 | 11.376 | 192.425 | 14.091 | 5.191 | 0.06× | 0.06× | 0.07× | 0.03× |
| Ackermann function | 8 | 7.787 | 7.680 | 208.689 | 7.411 | 2.288 | 0.04× | 0.04× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.565 | 0.724 | 12.771 | 6.511 | 0.751 | 0.12× | 0.06× | 0.51× | 0.06× |
| Quicksort | 30000 | 4.409 | 2.241 | 27.049 | 6.010 | 2.132 | 0.16× | 0.08× | 0.22× | 0.08× |
| Matrix multiplication | 150 | 6.395 | 2.258 | 212.011 | 8.823 | 1.957 | 0.03× | 0.01× | 0.04× | 0.01× |
| Mandelbrot set | 300 | 4.377 | 4.265 | 145.553 | 4.975 | 3.357 | 0.03× | 0.03× | 0.03× | 0.02× |
| N-Queens | 10 | 5.682 | 4.054 | 102.010 | 4.280 | 3.182 | 0.06× | 0.04× | 0.04× | 0.03× |
| Binary trees | 16 | 51.223 | 53.150 | 405.110 | 30.252 | 18.197 | 0.13× | 0.13× | 0.07× | 0.04× |
| Spectral norm | 250 | 5.190 | 4.236 | 274.686 | 8.559 | 3.089 | 0.02× | 0.02× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 15.798 | 18.045 | 606.020 | 46.663 | 17.020 | 0.03× | 0.03× | 0.08× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 11.376 | 14.091 | 1.24× | AquariusLang (typed), 1.24× faster |
| Ackermann function | 8 | 7.680 | 7.411 | 0.97× | Node.js, 1.04× faster |
| Sieve of Eratosthenes | 200000 | 0.724 | 6.511 | 8.99× | AquariusLang (typed), 8.99× faster |
| Quicksort | 30000 | 2.241 | 6.010 | 2.68× | AquariusLang (typed), 2.68× faster |
| Matrix multiplication | 150 | 2.258 | 8.823 | 3.91× | AquariusLang (typed), 3.91× faster |
| Mandelbrot set | 300 | 4.265 | 4.975 | 1.17× | AquariusLang (typed), 1.17× faster |
| N-Queens | 10 | 4.054 | 4.280 | 1.06× | AquariusLang (typed), 1.06× faster |
| Binary trees | 16 | 53.150 | 30.252 | 0.57× | Node.js, 1.76× faster |
| Spectral norm | 250 | 4.236 | 8.559 | 2.02× | AquariusLang (typed), 2.02× faster |
| Collatz conjecture | 100000 | 18.045 | 46.663 | 2.59× | AquariusLang (typed), 2.59× faster |
| **Geometric mean** | | | | **1.83×** | AquariusLang (typed), 1.83× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 10.227 | 12.441 | 0.998 | 8.9% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 10.055 | 14.179 | 1.517 | 13.0% | 5/5 |
| Recursive Fibonacci | Python | 182.646 | 195.855 | 5.114 | 2.7% | 5/5 |
| Recursive Fibonacci | Node.js | 13.700 | 17.522 | 1.699 | 11.3% | 5/5 |
| Recursive Fibonacci | C# | 4.892 | 5.749 | 0.388 | 7.3% | 5/5 |
| Ackermann function | AquariusLang | 7.604 | 8.264 | 0.267 | 3.4% | 5/5 |
| Ackermann function | AquariusLang (typed) | 7.397 | 8.555 | 0.447 | 5.7% | 5/5 |
| Ackermann function | Python | 198.002 | 217.470 | 7.404 | 3.5% | 5/5 |
| Ackermann function | Node.js | 7.397 | 8.490 | 0.533 | 6.8% | 5/5 |
| Ackermann function | C# | 2.178 | 2.406 | 0.091 | 4.0% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.363 | 1.688 | 0.126 | 8.2% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.704 | 1.008 | 0.137 | 16.9% | 5/5 |
| Sieve of Eratosthenes | Python | 12.148 | 13.433 | 0.565 | 4.4% | 5/5 |
| Sieve of Eratosthenes | Node.js | 5.689 | 6.871 | 0.483 | 7.5% | 5/5 |
| Sieve of Eratosthenes | C# | 0.694 | 0.800 | 0.049 | 6.6% | 5/5 |
| Quicksort | AquariusLang | 4.053 | 4.808 | 0.301 | 6.9% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.087 | 2.310 | 0.089 | 4.0% | 5/5 |
| Quicksort | Python | 25.828 | 28.157 | 0.896 | 3.3% | 5/5 |
| Quicksort | Node.js | 5.601 | 6.140 | 0.216 | 3.6% | 5/5 |
| Quicksort | C# | 1.977 | 2.743 | 0.296 | 13.3% | 5/5 |
| Matrix multiplication | AquariusLang | 5.423 | 7.447 | 0.778 | 12.3% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.053 | 2.495 | 0.162 | 7.1% | 5/5 |
| Matrix multiplication | Python | 200.418 | 222.159 | 7.886 | 3.7% | 5/5 |
| Matrix multiplication | Node.js | 7.774 | 9.056 | 0.548 | 6.4% | 5/5 |
| Matrix multiplication | C# | 1.858 | 2.049 | 0.075 | 3.9% | 5/5 |
| Mandelbrot set | AquariusLang | 4.200 | 4.647 | 0.162 | 3.7% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.076 | 4.444 | 0.132 | 3.1% | 5/5 |
| Mandelbrot set | Python | 135.244 | 168.298 | 12.403 | 8.4% | 5/5 |
| Mandelbrot set | Node.js | 4.942 | 5.313 | 0.155 | 3.1% | 5/5 |
| Mandelbrot set | C# | 3.177 | 3.744 | 0.208 | 6.1% | 5/5 |
| N-Queens | AquariusLang | 5.444 | 6.398 | 0.391 | 6.7% | 5/5 |
| N-Queens | AquariusLang (typed) | 3.792 | 4.229 | 0.173 | 4.3% | 5/5 |
| N-Queens | Python | 100.139 | 103.819 | 1.307 | 1.3% | 5/5 |
| N-Queens | Node.js | 4.159 | 5.026 | 0.358 | 8.0% | 5/5 |
| N-Queens | C# | 2.953 | 3.232 | 0.131 | 4.2% | 5/5 |
| Binary trees | AquariusLang | 47.367 | 60.688 | 5.159 | 9.8% | 5/5 |
| Binary trees | AquariusLang (typed) | 47.600 | 60.058 | 4.890 | 9.3% | 5/5 |
| Binary trees | Python | 311.518 | 442.833 | 54.430 | 14.2% | 5/5 |
| Binary trees | Node.js | 27.041 | 31.068 | 1.720 | 5.9% | 5/5 |
| Binary trees | C# | 15.548 | 20.136 | 1.934 | 10.9% | 5/5 |
| Spectral norm | AquariusLang | 4.802 | 5.920 | 0.414 | 7.9% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.980 | 4.510 | 0.220 | 5.2% | 5/5 |
| Spectral norm | Python | 259.373 | 280.485 | 8.535 | 3.1% | 5/5 |
| Spectral norm | Node.js | 8.087 | 10.933 | 1.290 | 14.0% | 5/5 |
| Spectral norm | C# | 2.911 | 3.176 | 0.100 | 3.2% | 5/5 |
| Collatz conjecture | AquariusLang | 15.739 | 19.059 | 1.664 | 9.8% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.435 | 18.771 | 0.537 | 3.0% | 5/5 |
| Collatz conjecture | Python | 581.718 | 641.194 | 26.383 | 4.3% | 5/5 |
| Collatz conjecture | Node.js | 43.722 | 50.223 | 2.610 | 5.6% | 5/5 |
| Collatz conjecture | C# | 16.563 | 17.674 | 0.420 | 2.5% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 56.10, Node.js 45.77, AquariusLang 43.32, Python 1.87 (higher is faster).**

Pairwise composite speed: C# is 1.78× as fast as AquariusLang (typed); C# is 2.18× as fast as Node.js; C# is 2.31× as fast as AquariusLang; C# is 53.55× as fast as Python; AquariusLang (typed) is 1.23× as fast as Node.js; AquariusLang (typed) is 1.29× as fast as AquariusLang; AquariusLang (typed) is 30.05× as fast as Python; Node.js is 1.06× as fast as AquariusLang; Node.js is 24.51× as fast as Python; AquariusLang is 23.20× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs Node.js | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.782× | 2.185× | 2.308× | 53.555× |
| 2 | AquariusLang (typed) | 56.10 | 0.561× | 1.000× | 1.226× | 1.295× | 30.047× |
| 3 | Node.js | 45.77 | 0.458× | 0.816× | 1.000× | 1.056× | 24.512× |
| 4 | AquariusLang | 43.32 | 0.433× | 0.772× | 0.947× | 1.000× | 23.202× |
| 5 | Python | 1.87 | 0.019× | 0.033× | 0.041× | 0.043× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 10.570 | 10.943 | 190.107 | 15.234 | 5.083 | 0.06× | 0.06× | 0.08× | 0.03× |
| Ackermann function | 8 | 7.922 | 7.400 | 212.914 | 7.725 | 2.001 | 0.04× | 0.03× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.233 | 0.777 | 13.461 | 2.387 | 0.381 | 0.09× | 0.06× | 0.18× | 0.03× |
| Quicksort | 30000 | 4.142 | 2.232 | 27.740 | 2.894 | 1.582 | 0.15× | 0.08× | 0.10× | 0.06× |
| Matrix multiplication | 150 | 6.176 | 2.372 | 218.130 | 3.216 | 1.682 | 0.03× | 0.01× | 0.01× | 0.01× |
| Mandelbrot set | 300 | 4.124 | 4.204 | 148.745 | 3.198 | 3.189 | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 10 | 6.039 | 4.234 | 100.625 | 3.886 | 2.893 | 0.06× | 0.04× | 0.04× | 0.03× |
| Binary trees | 16 | 44.882 | 42.281 | 423.882 | 14.470 | 15.978 | 0.11× | 0.10× | 0.03× | 0.04× |
| Spectral norm | 250 | 5.139 | 4.249 | 276.779 | 6.906 | 2.177 | 0.02× | 0.02× | 0.02× | 0.01× |
| Collatz conjecture | 100000 | 16.007 | 17.188 | 1896.481 | 43.184 | 17.112 | 0.01× | 0.01× | 0.02× | 0.01× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 10.943 | 15.234 | 1.39× | AquariusLang (typed), 1.39× faster |
| Ackermann function | 8 | 7.400 | 7.725 | 1.04× | AquariusLang (typed), 1.04× faster |
| Sieve of Eratosthenes | 200000 | 0.777 | 2.387 | 3.07× | AquariusLang (typed), 3.07× faster |
| Quicksort | 30000 | 2.232 | 2.894 | 1.30× | AquariusLang (typed), 1.30× faster |
| Matrix multiplication | 150 | 2.372 | 3.216 | 1.36× | AquariusLang (typed), 1.36× faster |
| Mandelbrot set | 300 | 4.204 | 3.198 | 0.76× | Node.js, 1.31× faster |
| N-Queens | 10 | 4.234 | 3.886 | 0.92× | Node.js, 1.09× faster |
| Binary trees | 16 | 42.281 | 14.470 | 0.34× | Node.js, 2.92× faster |
| Spectral norm | 250 | 4.249 | 6.906 | 1.63× | AquariusLang (typed), 1.63× faster |
| Collatz conjecture | 100000 | 17.188 | 43.184 | 2.51× | AquariusLang (typed), 2.51× faster |
| **Geometric mean** | | | | **1.23×** | AquariusLang (typed), 1.23× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 10.324 | 11.281 | 0.420 | 3.9% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 10.097 | 11.181 | 0.524 | 4.9% | 5/5 |
| Recursive Fibonacci | Python | 180.965 | 194.834 | 5.335 | 2.8% | 5/5 |
| Recursive Fibonacci | Node.js | 14.454 | 15.401 | 0.403 | 2.7% | 5/5 |
| Recursive Fibonacci | C# | 4.932 | 5.309 | 0.172 | 3.4% | 5/5 |
| Ackermann function | AquariusLang | 7.040 | 8.177 | 0.434 | 5.6% | 5/5 |
| Ackermann function | AquariusLang (typed) | 7.063 | 7.578 | 0.188 | 2.6% | 5/5 |
| Ackermann function | Python | 205.321 | 247.826 | 17.682 | 8.1% | 5/5 |
| Ackermann function | Node.js | 6.958 | 8.818 | 0.766 | 9.9% | 5/5 |
| Ackermann function | C# | 1.913 | 2.270 | 0.147 | 7.2% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.186 | 1.673 | 0.217 | 16.0% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.734 | 0.941 | 0.082 | 10.2% | 5/5 |
| Sieve of Eratosthenes | Python | 12.551 | 13.920 | 0.554 | 4.2% | 5/5 |
| Sieve of Eratosthenes | Node.js | 2.330 | 2.464 | 0.049 | 2.0% | 5/5 |
| Sieve of Eratosthenes | C# | 0.357 | 0.407 | 0.020 | 5.4% | 5/5 |
| Quicksort | AquariusLang | 4.075 | 4.469 | 0.175 | 4.2% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.136 | 2.307 | 0.076 | 3.4% | 5/5 |
| Quicksort | Python | 27.268 | 28.455 | 0.440 | 1.6% | 5/5 |
| Quicksort | Node.js | 2.740 | 3.121 | 0.146 | 5.0% | 5/5 |
| Quicksort | C# | 1.440 | 1.741 | 0.107 | 6.8% | 5/5 |
| Matrix multiplication | AquariusLang | 5.857 | 6.670 | 0.298 | 4.8% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.246 | 2.488 | 0.091 | 3.8% | 5/5 |
| Matrix multiplication | Python | 216.285 | 227.140 | 4.276 | 1.9% | 5/5 |
| Matrix multiplication | Node.js | 2.846 | 4.585 | 0.666 | 19.3% | 5/5 |
| Matrix multiplication | C# | 1.656 | 2.085 | 0.184 | 10.5% | 5/5 |
| Mandelbrot set | AquariusLang | 4.005 | 4.472 | 0.186 | 4.4% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.065 | 4.720 | 0.265 | 6.2% | 5/5 |
| Mandelbrot set | Python | 144.085 | 155.867 | 4.247 | 2.8% | 5/5 |
| Mandelbrot set | Node.js | 3.037 | 3.304 | 0.101 | 3.2% | 5/5 |
| Mandelbrot set | C# | 3.015 | 3.260 | 0.096 | 3.1% | 5/5 |
| N-Queens | AquariusLang | 5.456 | 6.485 | 0.453 | 7.5% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.046 | 4.374 | 0.122 | 2.9% | 5/5 |
| N-Queens | Python | 95.752 | 103.001 | 2.667 | 2.7% | 5/5 |
| N-Queens | Node.js | 3.639 | 3.954 | 0.121 | 3.1% | 5/5 |
| N-Queens | C# | 2.668 | 3.045 | 0.160 | 5.6% | 5/5 |
| Binary trees | AquariusLang | 40.168 | 59.884 | 9.385 | 18.9% | 5/5 |
| Binary trees | AquariusLang (typed) | 39.927 | 54.601 | 6.485 | 14.1% | 5/5 |
| Binary trees | Python | 358.221 | 953.220 | 247.281 | 45.8% | 5/5 |
| Binary trees | Node.js | 14.014 | 16.327 | 0.927 | 6.3% | 5/5 |
| Binary trees | C# | 15.095 | 17.881 | 1.048 | 6.5% | 5/5 |
| Spectral norm | AquariusLang | 4.954 | 5.504 | 0.247 | 4.7% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.940 | 4.274 | 0.141 | 3.4% | 5/5 |
| Spectral norm | Python | 268.280 | 286.331 | 6.935 | 2.5% | 5/5 |
| Spectral norm | Node.js | 6.710 | 7.632 | 0.386 | 5.4% | 5/5 |
| Spectral norm | C# | 2.057 | 2.235 | 0.077 | 3.5% | 5/5 |
| Collatz conjecture | AquariusLang | 15.847 | 17.218 | 0.579 | 3.6% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 16.938 | 19.315 | 0.970 | 5.5% | 5/5 |
| Collatz conjecture | Python | 1209.255 | 2308.248 | 462.073 | 25.4% | 5/5 |
| Collatz conjecture | Node.js | 42.267 | 46.641 | 1.756 | 4.0% | 5/5 |
| Collatz conjecture | C# | 16.864 | 18.911 | 0.856 | 4.9% | 5/5 |

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
- AquariusLang always builds the Wasm with `aqua build` before measuring, then runs `aqua run`; Wasm generation is not part of the sample time, and each mode's copy is built separately. "AquariusLang (typed)" uses the same compiler and the same algorithms, adding only optional type annotations on variables, parameters and return values (`benchmarks/aquarius_typed/`); typed functions must declare a return type, so the in-place functions of quicksort and spectral norm gain a `回傳 0;` (`return 0;`) line, and binary trees annotate the tree arrays as `陣列` (`Array`, an array whose elements can be any value). The input size `benchmark_n` is declared `常數` (`const`), the counterpart of C#'s `static readonly int benchmark_n`, which the JIT treats as a constant; this needs a compiler that supports `常數`, and the untyped scripts keep `變數`. Python runs the source, and Node.js uses V8. C# is compiled ahead of time into a net8.0 assembly with `dotnet build --configuration Release` and run directly as `dotnet Benchmark.dll`; build and restore are not timed, and no external NuGet packages are used. The initial JIT before Main is not timed; on-demand JIT inside the timed interval still counts. The assembly turns tiered compilation off (`TieredCompilation=false`), so each method is compiled by the optimizing JIT on its first call, matching the optimized Wasmtime compilation AquariusLang finishes before timing. No NumPy, native algorithm libraries, worker threads or built-in sorts are used.
- Warm-up process samples are discarded; they warm the operating system's file cache, and no JIT or VM state carries over between processes. Each round shuffles every algorithm, language and mode combination with the recorded random seed, then runs them in that order.
- Every timed run of every warm-up and counted sample must match the untimed Python reference answer. Integers must be identical; the squared spectral norm allows a relative error of 1e-9 and an absolute error of 1e-12. A non-zero exit code, a timeout, missing or extra standard output, a non-finite value or a checksum mismatch fails the test. The timing output must be a finite millisecond value above zero; a missing timing does not fall back to whole-process timing.
- AquariusLang's integer `/` truncates; Python uses `//` and Node.js `Math.trunc` to match. Floating-point tests use double precision (AquariusLang uses `d` literals); at the standard size every intermediate integer stays within the signed 32-bit range.
- Array construction has the same linear cost in every language: AquariusLang preallocates with `陣列.建立` (`Array.Make`; quicksort uses `陣列.追加`, `Array.Append`, with reserved capacity), Python uses `[value] * n` / `append`, Node.js `push`, C# `new T[n]` (with `Array.Fill` where needed); no append that copies the whole array each time is used.
- Compilation timing: Wasmtime has fully compiled the AquariusLang Wasm to machine code before timing starts. C# has tiered compilation off, so methods are compiled by the optimizing JIT on their first call; in standard mode that JIT is still inside the timed interval. Node.js (V8) cannot optimize ahead of time and starts in its interpreter and baseline compiler; in standard mode hot functions are optimized inside the timed interval, which favors AquariusLang; warmed mode relies on in-process warm-up to optimize hot functions before timing, though a little JIT or garbage collection may still fall inside the timed interval. At the standard size each test takes about 1 millisecond, so timer and allocation noise weigh more; `--profile large` reduces this with larger inputs, and the scores of the two sizes must not be mixed.
- Small workloads can be affected by timer and function call costs; warmed mode warms up only a few times and is not the steady-state speed of a long run, while standard mode reflects only the first run; neither represents a language ranking for every program. CPU frequency, temperature, background work and scheduling noise are not controlled. Process memory use and CPU time are not measured; the RAM below is the machine's installed memory.

## Test date and environment

- Started: 2026-11-02T12:52:59.431456+08:00
- Finished: 2026-11-02T12:58:47.163512+08:00
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
| AquariusLang | no version option; identified by release folder and binary hashes | C:\OfficialProjects\aqua-perf-final-preempt\aqua.exe |
| AquariusLang (typed) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\aqua-perf-final-preempt\aqua.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.exe |
| C# | SDKs: 8.0.426 [C:\Program Files\dotnet\sdk] Runtimes: Microsoft.AspNetCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App] Microsoft.NETCore.App 6.0.36 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.WindowsDesktop.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] Microsoft.WindowsDesktop.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] | C:\Program Files\dotnet\dotnet.exe |

AquariusLang release folder: `C:\OfficialProjects\aqua-perf-final-preempt`.

AquariusLang launcher SHA-256: `0a69f4a2cac56a7544502fbb11fdd0ff52f48f6580a2d0fccf80f451259340ef`.


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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final-preempt\20261102-125259-431456\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final-preempt\20261102-125259-431456\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final-preempt\20261102-125259-431456\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

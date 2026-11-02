# Desktop performance benchmark: AquariusLang, AquariusLang (typed), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: C# 100.00, AquariusLang (typed) 68.42, AquariusLang 51.60, Node.js 36.42, Python 2.69
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 59.28, Node.js 44.51, AquariusLang 43.09, Python 2.18

The project provides ten classic algorithms, 50 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: C# 100.00, AquariusLang (typed) 68.42, AquariusLang 51.60, Node.js 36.42, Python 2.69 (higher is faster).**

Pairwise composite speed: C# is 1.46× as fast as AquariusLang (typed); C# is 1.94× as fast as AquariusLang; C# is 2.75× as fast as Node.js; C# is 37.13× as fast as Python; AquariusLang (typed) is 1.33× as fast as AquariusLang; AquariusLang (typed) is 1.88× as fast as Node.js; AquariusLang (typed) is 25.40× as fast as Python; AquariusLang is 1.42× as fast as Node.js; AquariusLang is 19.16× as fast as Python; Node.js is 13.52× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.462× | 1.938× | 2.746× | 37.127× |
| 2 | AquariusLang (typed) | 68.42 | 0.684× | 1.000× | 1.326× | 1.879× | 25.402× |
| 3 | AquariusLang | 51.60 | 0.516× | 0.754× | 1.000× | 1.417× | 19.158× |
| 4 | Node.js | 36.42 | 0.364× | 0.532× | 0.706× | 1.000× | 13.522× |
| 5 | Python | 2.69 | 0.027× | 0.039× | 0.052× | 0.074× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 10.172 | 10.120 | 178.591 | 14.293 | 5.263 | 0.06× | 0.06× | 0.08× | 0.03× |
| Ackermann function | 8 | 6.738 | 6.891 | 199.227 | 7.126 | 2.157 | 0.03× | 0.03× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.415 | 0.752 | 12.454 | 5.565 | 0.750 | 0.11× | 0.06× | 0.45× | 0.06× |
| Quicksort | 30000 | 3.976 | 2.251 | 25.768 | 6.542 | 2.156 | 0.15× | 0.09× | 0.25× | 0.08× |
| Matrix multiplication | 150 | 5.953 | 2.140 | 206.816 | 8.472 | 1.970 | 0.03× | 0.01× | 0.04× | 0.01× |
| Mandelbrot set | 300 | 4.009 | 4.176 | 134.538 | 4.879 | 3.126 | 0.03× | 0.03× | 0.04× | 0.02× |
| N-Queens | 10 | 5.630 | 4.065 | 98.489 | 4.319 | 3.123 | 0.06× | 0.04× | 0.04× | 0.03× |
| Binary trees | 16 | 47.046 | 39.874 | 274.405 | 28.931 | 14.958 | 0.17× | 0.15× | 0.11× | 0.05× |
| Spectral norm | 250 | 5.345 | 4.011 | 261.693 | 7.902 | 3.029 | 0.02× | 0.02× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 15.740 | 17.792 | 607.640 | 44.157 | 17.139 | 0.03× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 10.120 | 14.293 | 1.41× | AquariusLang (typed), 1.41× faster |
| Ackermann function | 8 | 6.891 | 7.126 | 1.03× | AquariusLang (typed), 1.03× faster |
| Sieve of Eratosthenes | 200000 | 0.752 | 5.565 | 7.40× | AquariusLang (typed), 7.40× faster |
| Quicksort | 30000 | 2.251 | 6.542 | 2.91× | AquariusLang (typed), 2.91× faster |
| Matrix multiplication | 150 | 2.140 | 8.472 | 3.96× | AquariusLang (typed), 3.96× faster |
| Mandelbrot set | 300 | 4.176 | 4.879 | 1.17× | AquariusLang (typed), 1.17× faster |
| N-Queens | 10 | 4.065 | 4.319 | 1.06× | AquariusLang (typed), 1.06× faster |
| Binary trees | 16 | 39.874 | 28.931 | 0.73× | Node.js, 1.38× faster |
| Spectral norm | 250 | 4.011 | 7.902 | 1.97× | AquariusLang (typed), 1.97× faster |
| Collatz conjecture | 100000 | 17.792 | 44.157 | 2.48× | AquariusLang (typed), 2.48× faster |
| **Geometric mean** | | | | **1.88×** | AquariusLang (typed), 1.88× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 9.388 | 12.469 | 1.415 | 13.3% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 9.878 | 11.547 | 0.674 | 6.5% | 5/5 |
| Recursive Fibonacci | Python | 174.840 | 189.545 | 7.004 | 3.9% | 5/5 |
| Recursive Fibonacci | Node.js | 13.405 | 15.941 | 1.135 | 7.8% | 5/5 |
| Recursive Fibonacci | C# | 4.874 | 5.288 | 0.196 | 3.8% | 5/5 |
| Ackermann function | AquariusLang | 6.400 | 7.027 | 0.241 | 3.6% | 5/5 |
| Ackermann function | AquariusLang (typed) | 6.291 | 7.480 | 0.445 | 6.5% | 5/5 |
| Ackermann function | Python | 191.533 | 216.754 | 9.795 | 4.8% | 5/5 |
| Ackermann function | Node.js | 6.883 | 7.384 | 0.212 | 3.0% | 5/5 |
| Ackermann function | C# | 2.094 | 2.357 | 0.105 | 4.8% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.315 | 1.501 | 0.066 | 4.7% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.721 | 0.783 | 0.025 | 3.4% | 5/5 |
| Sieve of Eratosthenes | Python | 12.177 | 17.611 | 2.335 | 16.9% | 5/5 |
| Sieve of Eratosthenes | Node.js | 5.337 | 5.940 | 0.221 | 4.0% | 5/5 |
| Sieve of Eratosthenes | C# | 0.682 | 0.827 | 0.058 | 7.9% | 5/5 |
| Quicksort | AquariusLang | 3.854 | 4.392 | 0.238 | 5.8% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.110 | 2.271 | 0.068 | 3.1% | 5/5 |
| Quicksort | Python | 24.080 | 28.834 | 1.920 | 7.3% | 5/5 |
| Quicksort | Node.js | 5.689 | 19.979 | 6.061 | 64.3% | 5/5 |
| Quicksort | C# | 1.905 | 2.283 | 0.148 | 6.9% | 5/5 |
| Matrix multiplication | AquariusLang | 5.650 | 6.803 | 0.471 | 7.8% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.031 | 2.190 | 0.068 | 3.2% | 5/5 |
| Matrix multiplication | Python | 195.936 | 242.272 | 18.385 | 8.7% | 5/5 |
| Matrix multiplication | Node.js | 8.323 | 9.127 | 0.313 | 3.6% | 5/5 |
| Matrix multiplication | C# | 1.944 | 2.008 | 0.025 | 1.2% | 5/5 |
| Mandelbrot set | AquariusLang | 3.945 | 4.501 | 0.239 | 5.7% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.110 | 7.579 | 1.524 | 31.4% | 5/5 |
| Mandelbrot set | Python | 133.197 | 143.874 | 5.229 | 3.8% | 5/5 |
| Mandelbrot set | Node.js | 4.754 | 5.160 | 0.154 | 3.1% | 5/5 |
| Mandelbrot set | C# | 3.094 | 3.395 | 0.122 | 3.8% | 5/5 |
| N-Queens | AquariusLang | 5.387 | 6.857 | 0.588 | 10.1% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.034 | 5.396 | 0.584 | 13.3% | 5/5 |
| N-Queens | Python | 94.327 | 102.558 | 3.489 | 3.5% | 5/5 |
| N-Queens | Node.js | 4.193 | 4.576 | 0.141 | 3.3% | 5/5 |
| N-Queens | C# | 3.062 | 3.295 | 0.088 | 2.8% | 5/5 |
| Binary trees | AquariusLang | 45.297 | 49.023 | 1.379 | 2.9% | 5/5 |
| Binary trees | AquariusLang (typed) | 37.501 | 42.029 | 1.676 | 4.2% | 5/5 |
| Binary trees | Python | 263.345 | 313.487 | 20.006 | 7.1% | 5/5 |
| Binary trees | Node.js | 23.797 | 37.439 | 5.234 | 17.5% | 5/5 |
| Binary trees | C# | 14.704 | 15.934 | 0.478 | 3.2% | 5/5 |
| Spectral norm | AquariusLang | 5.142 | 6.565 | 0.596 | 10.8% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.743 | 4.123 | 0.148 | 3.7% | 5/5 |
| Spectral norm | Python | 252.095 | 277.739 | 10.590 | 4.0% | 5/5 |
| Spectral norm | Node.js | 7.184 | 10.145 | 1.151 | 14.0% | 5/5 |
| Spectral norm | C# | 2.947 | 3.480 | 0.222 | 7.1% | 5/5 |
| Collatz conjecture | AquariusLang | 14.872 | 16.806 | 0.803 | 5.1% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.394 | 18.211 | 0.318 | 1.8% | 5/5 |
| Collatz conjecture | Python | 584.635 | 691.529 | 43.541 | 7.0% | 5/5 |
| Collatz conjecture | Node.js | 42.995 | 44.929 | 0.830 | 1.9% | 5/5 |
| Collatz conjecture | C# | 16.462 | 19.428 | 1.200 | 6.9% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 59.28, Node.js 44.51, AquariusLang 43.09, Python 2.18 (higher is faster).**

Pairwise composite speed: C# is 1.69× as fast as AquariusLang (typed); C# is 2.25× as fast as Node.js; C# is 2.32× as fast as AquariusLang; C# is 45.86× as fast as Python; AquariusLang (typed) is 1.33× as fast as Node.js; AquariusLang (typed) is 1.38× as fast as AquariusLang; AquariusLang (typed) is 27.18× as fast as Python; Node.js is 1.03× as fast as AquariusLang; Node.js is 20.41× as fast as Python; AquariusLang is 19.76× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs Node.js | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.687× | 2.247× | 2.320× | 45.855× |
| 2 | AquariusLang (typed) | 59.28 | 0.593× | 1.000× | 1.332× | 1.376× | 27.183× |
| 3 | Node.js | 44.51 | 0.445× | 0.751× | 1.000× | 1.033× | 20.408× |
| 4 | AquariusLang | 43.09 | 0.431× | 0.727× | 0.968× | 1.000× | 19.761× |
| 5 | Python | 2.18 | 0.022× | 0.037× | 0.049× | 0.051× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 10.072 | 10.214 | 184.181 | 14.414 | 5.052 | 0.05× | 0.06× | 0.08× | 0.03× |
| Ackermann function | 8 | 6.564 | 6.597 | 204.743 | 7.177 | 2.015 | 0.03× | 0.03× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.214 | 0.782 | 13.463 | 2.323 | 0.379 | 0.09× | 0.06× | 0.17× | 0.03× |
| Quicksort | 30000 | 4.250 | 2.288 | 25.977 | 2.835 | 1.448 | 0.16× | 0.09× | 0.11× | 0.06× |
| Matrix multiplication | 150 | 5.951 | 2.174 | 207.463 | 4.567 | 1.750 | 0.03× | 0.01× | 0.02× | 0.01× |
| Mandelbrot set | 300 | 4.170 | 4.153 | 137.381 | 3.122 | 3.108 | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 10 | 5.686 | 4.142 | 96.755 | 3.731 | 2.721 | 0.06× | 0.04× | 0.04× | 0.03× |
| Binary trees | 16 | 51.985 | 26.244 | 299.212 | 13.500 | 14.258 | 0.17× | 0.09× | 0.05× | 0.05× |
| Spectral norm | 250 | 5.040 | 3.918 | 276.552 | 6.748 | 2.062 | 0.02× | 0.01× | 0.02× | 0.01× |
| Collatz conjecture | 100000 | 15.547 | 17.448 | 591.936 | 43.053 | 17.798 | 0.03× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 10.214 | 14.414 | 1.41× | AquariusLang (typed), 1.41× faster |
| Ackermann function | 8 | 6.597 | 7.177 | 1.09× | AquariusLang (typed), 1.09× faster |
| Sieve of Eratosthenes | 200000 | 0.782 | 2.323 | 2.97× | AquariusLang (typed), 2.97× faster |
| Quicksort | 30000 | 2.288 | 2.835 | 1.24× | AquariusLang (typed), 1.24× faster |
| Matrix multiplication | 150 | 2.174 | 4.567 | 2.10× | AquariusLang (typed), 2.10× faster |
| Mandelbrot set | 300 | 4.153 | 3.122 | 0.75× | Node.js, 1.33× faster |
| N-Queens | 10 | 4.142 | 3.731 | 0.90× | Node.js, 1.11× faster |
| Binary trees | 16 | 26.244 | 13.500 | 0.51× | Node.js, 1.94× faster |
| Spectral norm | 250 | 3.918 | 6.748 | 1.72× | AquariusLang (typed), 1.72× faster |
| Collatz conjecture | 100000 | 17.448 | 43.053 | 2.47× | AquariusLang (typed), 2.47× faster |
| **Geometric mean** | | | | **1.33×** | AquariusLang (typed), 1.33× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 9.952 | 10.459 | 0.202 | 2.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 9.805 | 10.835 | 0.389 | 3.8% | 5/5 |
| Recursive Fibonacci | Python | 172.391 | 194.041 | 8.408 | 4.6% | 5/5 |
| Recursive Fibonacci | Node.js | 13.814 | 15.169 | 0.654 | 4.5% | 5/5 |
| Recursive Fibonacci | C# | 4.883 | 5.273 | 0.153 | 3.0% | 5/5 |
| Ackermann function | AquariusLang | 6.386 | 7.037 | 0.288 | 4.3% | 5/5 |
| Ackermann function | AquariusLang (typed) | 6.461 | 7.092 | 0.247 | 3.7% | 5/5 |
| Ackermann function | Python | 196.155 | 210.006 | 6.745 | 3.3% | 5/5 |
| Ackermann function | Node.js | 6.937 | 8.025 | 0.439 | 6.0% | 5/5 |
| Ackermann function | C# | 1.900 | 2.167 | 0.105 | 5.3% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.153 | 1.379 | 0.086 | 7.0% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.764 | 0.982 | 0.091 | 11.1% | 5/5 |
| Sieve of Eratosthenes | Python | 12.123 | 13.772 | 0.763 | 5.8% | 5/5 |
| Sieve of Eratosthenes | Node.js | 2.256 | 2.399 | 0.058 | 2.5% | 5/5 |
| Sieve of Eratosthenes | C# | 0.371 | 0.390 | 0.008 | 2.0% | 5/5 |
| Quicksort | AquariusLang | 4.040 | 4.426 | 0.175 | 4.1% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.225 | 2.358 | 0.048 | 2.1% | 5/5 |
| Quicksort | Python | 24.759 | 28.606 | 1.727 | 6.5% | 5/5 |
| Quicksort | Node.js | 2.742 | 2.955 | 0.089 | 3.1% | 5/5 |
| Quicksort | C# | 1.440 | 1.597 | 0.068 | 4.6% | 5/5 |
| Matrix multiplication | AquariusLang | 5.327 | 6.240 | 0.358 | 6.1% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.115 | 2.209 | 0.037 | 1.7% | 5/5 |
| Matrix multiplication | Python | 202.222 | 223.726 | 8.706 | 4.1% | 5/5 |
| Matrix multiplication | Node.js | 2.911 | 4.864 | 0.976 | 24.2% | 5/5 |
| Matrix multiplication | C# | 1.700 | 1.811 | 0.051 | 2.9% | 5/5 |
| Mandelbrot set | AquariusLang | 4.150 | 4.342 | 0.079 | 1.9% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 3.929 | 4.253 | 0.126 | 3.0% | 5/5 |
| Mandelbrot set | Python | 132.715 | 146.512 | 5.326 | 3.8% | 5/5 |
| Mandelbrot set | Node.js | 2.987 | 3.166 | 0.083 | 2.7% | 5/5 |
| Mandelbrot set | C# | 2.963 | 3.227 | 0.109 | 3.5% | 5/5 |
| N-Queens | AquariusLang | 5.457 | 7.187 | 0.722 | 12.0% | 5/5 |
| N-Queens | AquariusLang (typed) | 3.961 | 4.315 | 0.145 | 3.5% | 5/5 |
| N-Queens | Python | 94.208 | 136.343 | 17.901 | 17.1% | 5/5 |
| N-Queens | Node.js | 3.585 | 3.950 | 0.133 | 3.5% | 5/5 |
| N-Queens | C# | 2.654 | 3.014 | 0.154 | 5.5% | 5/5 |
| Binary trees | AquariusLang | 42.881 | 57.445 | 5.469 | 10.9% | 5/5 |
| Binary trees | AquariusLang (typed) | 23.260 | 30.443 | 2.899 | 11.1% | 5/5 |
| Binary trees | Python | 268.587 | 318.183 | 20.078 | 6.8% | 5/5 |
| Binary trees | Node.js | 11.826 | 14.371 | 1.123 | 8.6% | 5/5 |
| Binary trees | C# | 13.931 | 14.630 | 0.249 | 1.7% | 5/5 |
| Spectral norm | AquariusLang | 4.924 | 5.438 | 0.201 | 3.9% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.758 | 4.239 | 0.184 | 4.7% | 5/5 |
| Spectral norm | Python | 259.423 | 283.053 | 9.406 | 3.4% | 5/5 |
| Spectral norm | Node.js | 6.694 | 7.311 | 0.261 | 3.8% | 5/5 |
| Spectral norm | C# | 2.051 | 2.116 | 0.027 | 1.3% | 5/5 |
| Collatz conjecture | AquariusLang | 14.702 | 16.388 | 0.648 | 4.2% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.028 | 18.419 | 0.636 | 3.6% | 5/5 |
| Collatz conjecture | Python | 573.146 | 616.182 | 18.927 | 3.2% | 5/5 |
| Collatz conjecture | Node.js | 41.572 | 45.461 | 1.754 | 4.0% | 5/5 |
| Collatz conjecture | C# | 16.459 | 17.929 | 0.706 | 4.1% | 5/5 |

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

- Started: 2026-11-02T11:55:38.646607+08:00
- Finished: 2026-11-02T12:00:22.623319+08:00
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
| AquariusLang | no version option; identified by release folder and binary hashes | C:\OfficialProjects\aqua-perf-final\aqua.exe |
| AquariusLang (typed) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\aqua-perf-final\aqua.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.exe |
| C# | SDKs: 8.0.426 [C:\Program Files\dotnet\sdk] Runtimes: Microsoft.AspNetCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App] Microsoft.NETCore.App 6.0.36 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.WindowsDesktop.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] Microsoft.WindowsDesktop.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] | C:\Program Files\dotnet\dotnet.exe |

AquariusLang release folder: `C:\OfficialProjects\aqua-perf-final`.

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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final\20261102-115538-646607\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final\20261102-115538-646607\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\csharp-parity-final\20261102-115538-646607\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

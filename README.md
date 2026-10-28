# Desktop performance benchmark: AquariusLang, AquariusLang (typed), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

> **Note: at the standard size most tests take about 1 millisecond, so the results mainly reflect a short program's latency after start-up (JIT warm-up, initial memory allocation), not sustained speed. To compare language speed, use `--profile large`.**

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: AquariusLang (typed) 100.00, AquariusLang 85.12, C# 65.28, Node.js 27.09, Python 5.29
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 49.04, Node.js 41.43, AquariusLang 37.65, Python 2.13

The project provides ten classic algorithms, 50 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: AquariusLang (typed) 100.00, AquariusLang 85.12, C# 65.28, Node.js 27.09, Python 5.29 (higher is faster).**

Pairwise composite speed: AquariusLang (typed) is 1.17× as fast as AquariusLang; AquariusLang (typed) is 1.53× as fast as C#; AquariusLang (typed) is 3.69× as fast as Node.js; AquariusLang (typed) is 18.92× as fast as Python; AquariusLang is 1.30× as fast as C#; AquariusLang is 3.14× as fast as Node.js; AquariusLang is 16.10× as fast as Python; C# is 2.41× as fast as Node.js; C# is 12.35× as fast as Python; Node.js is 5.12× as fast as Python.

| Rank | Language | Composite score | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs C# | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | AquariusLang (typed) | 100.00 | 1.000× | 1.175× | 1.532× | 3.691× | 18.915× |
| 2 | AquariusLang | 85.12 | 0.851× | 1.000× | 1.304× | 3.142× | 16.101× |
| 3 | C# | 65.28 | 0.653× | 0.767× | 1.000× | 2.410× | 12.348× |
| 4 | Node.js | 27.09 | 0.271× | 0.318× | 0.415× | 1.000× | 5.124× |
| 5 | Python | 5.29 | 0.053× | 0.062× | 0.081× | 0.195× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 28 | 1.562 | 1.691 | 33.336 | 2.429 | 0.832 | 0.05× | 0.05× | 0.07× | 0.02× |
| Ackermann function | 6 | 0.747 | 0.731 | 10.813 | 0.667 | 0.241 | 0.07× | 0.07× | 0.06× | 0.02× |
| Sieve of Eratosthenes | 10000 | 0.081 | 0.042 | 0.570 | 0.656 | 0.477 | 0.14× | 0.07× | 1.15× | 0.84× |
| Quicksort | 2000 | 0.257 | 0.129 | 1.440 | 0.946 | 0.537 | 0.18× | 0.09× | 0.66× | 0.37× |
| Matrix multiplication | 45 | 0.253 | 0.136 | 5.575 | 1.362 | 0.302 | 0.05× | 0.02× | 0.24× | 0.05× |
| Mandelbrot set | 80 | 0.314 | 0.327 | 12.132 | 1.053 | 0.379 | 0.03× | 0.03× | 0.09× | 0.03× |
| N-Queens | 8 | 0.230 | 0.250 | 3.595 | 0.842 | 0.410 | 0.06× | 0.07× | 0.23× | 0.11× |
| Binary trees | 12 | 2.346 | 2.448 | 8.904 | 3.510 | 1.516 | 0.26× | 0.27× | 0.39× | 0.17× |
| Spectral norm | 60 | 0.298 | 0.276 | 15.287 | 1.681 | 1.165 | 0.02× | 0.02× | 0.11× | 0.08× |
| Collatz conjecture | 10000 | 1.359 | 1.658 | 50.573 | 5.547 | 1.410 | 0.03× | 0.03× | 0.11× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 28 | 1.691 | 2.429 | 1.44× | AquariusLang (typed), 1.44× faster |
| Ackermann function | 6 | 0.731 | 0.667 | 0.91× | Node.js, 1.10× faster |
| Sieve of Eratosthenes | 10000 | 0.042 | 0.656 | 15.43× | AquariusLang (typed), 15.43× faster |
| Quicksort | 2000 | 0.129 | 0.946 | 7.31× | AquariusLang (typed), 7.31× faster |
| Matrix multiplication | 45 | 0.136 | 1.362 | 10.02× | AquariusLang (typed), 10.02× faster |
| Mandelbrot set | 80 | 0.327 | 1.053 | 3.22× | AquariusLang (typed), 3.22× faster |
| N-Queens | 8 | 0.250 | 0.842 | 3.37× | AquariusLang (typed), 3.37× faster |
| Binary trees | 12 | 2.448 | 3.510 | 1.43× | AquariusLang (typed), 1.43× faster |
| Spectral norm | 60 | 0.276 | 1.681 | 6.09× | AquariusLang (typed), 6.09× faster |
| Collatz conjecture | 10000 | 1.658 | 5.547 | 3.35× | AquariusLang (typed), 3.35× faster |
| **Geometric mean** | | | | **3.69×** | AquariusLang (typed), 3.69× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 1.558 | 1.747 | 0.081 | 5.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 1.565 | 2.134 | 0.262 | 14.5% | 5/5 |
| Recursive Fibonacci | Python | 28.826 | 61.629 | 13.127 | 34.0% | 5/5 |
| Recursive Fibonacci | Node.js | 2.341 | 3.148 | 0.410 | 15.3% | 5/5 |
| Recursive Fibonacci | C# | 0.824 | 1.118 | 0.153 | 16.3% | 5/5 |
| Ackermann function | AquariusLang | 0.553 | 0.814 | 0.099 | 13.7% | 5/5 |
| Ackermann function | AquariusLang (typed) | 0.557 | 0.738 | 0.097 | 14.5% | 5/5 |
| Ackermann function | Python | 10.658 | 11.151 | 0.183 | 1.7% | 5/5 |
| Ackermann function | Node.js | 0.654 | 0.949 | 0.144 | 18.9% | 5/5 |
| Ackermann function | C# | 0.230 | 0.389 | 0.069 | 24.7% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 0.075 | 0.102 | 0.011 | 13.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.039 | 0.050 | 0.005 | 11.5% | 5/5 |
| Sieve of Eratosthenes | Python | 0.565 | 1.034 | 0.205 | 29.3% | 5/5 |
| Sieve of Eratosthenes | Node.js | 0.569 | 1.113 | 0.224 | 30.8% | 5/5 |
| Sieve of Eratosthenes | C# | 0.358 | 0.486 | 0.065 | 15.0% | 5/5 |
| Quicksort | AquariusLang | 0.255 | 0.275 | 0.009 | 3.4% | 5/5 |
| Quicksort | AquariusLang (typed) | 0.123 | 0.191 | 0.030 | 20.4% | 5/5 |
| Quicksort | Python | 1.314 | 1.806 | 0.201 | 13.5% | 5/5 |
| Quicksort | Node.js | 0.840 | 1.035 | 0.079 | 8.3% | 5/5 |
| Quicksort | C# | 0.526 | 0.593 | 0.028 | 5.1% | 5/5 |
| Matrix multiplication | AquariusLang | 0.199 | 0.451 | 0.104 | 38.2% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 0.128 | 0.192 | 0.026 | 17.9% | 5/5 |
| Matrix multiplication | Python | 5.274 | 7.343 | 0.850 | 14.5% | 5/5 |
| Matrix multiplication | Node.js | 1.294 | 1.531 | 0.094 | 6.8% | 5/5 |
| Matrix multiplication | C# | 0.287 | 0.336 | 0.019 | 6.4% | 5/5 |
| Mandelbrot set | AquariusLang | 0.311 | 0.361 | 0.021 | 6.6% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 0.312 | 0.414 | 0.052 | 14.6% | 5/5 |
| Mandelbrot set | Python | 9.582 | 13.009 | 1.547 | 13.5% | 5/5 |
| Mandelbrot set | Node.js | 0.920 | 1.258 | 0.133 | 12.7% | 5/5 |
| Mandelbrot set | C# | 0.371 | 0.494 | 0.053 | 13.1% | 5/5 |
| N-Queens | AquariusLang | 0.227 | 0.238 | 0.004 | 1.9% | 5/5 |
| N-Queens | AquariusLang (typed) | 0.195 | 0.273 | 0.036 | 15.2% | 5/5 |
| N-Queens | Python | 3.548 | 4.128 | 0.245 | 6.6% | 5/5 |
| N-Queens | Node.js | 0.678 | 1.118 | 0.183 | 21.3% | 5/5 |
| N-Queens | C# | 0.372 | 0.693 | 0.138 | 28.9% | 5/5 |
| Binary trees | AquariusLang | 2.135 | 3.432 | 0.533 | 21.4% | 5/5 |
| Binary trees | AquariusLang (typed) | 2.153 | 2.596 | 0.187 | 7.8% | 5/5 |
| Binary trees | Python | 8.097 | 10.721 | 1.033 | 11.4% | 5/5 |
| Binary trees | Node.js | 3.062 | 4.412 | 0.600 | 16.2% | 5/5 |
| Binary trees | C# | 1.416 | 1.853 | 0.186 | 11.8% | 5/5 |
| Spectral norm | AquariusLang | 0.279 | 0.476 | 0.101 | 28.1% | 5/5 |
| Spectral norm | AquariusLang (typed) | 0.266 | 0.422 | 0.071 | 22.2% | 5/5 |
| Spectral norm | Python | 13.629 | 18.444 | 2.009 | 12.5% | 5/5 |
| Spectral norm | Node.js | 1.494 | 13.266 | 5.947 | 101.2% | 5/5 |
| Spectral norm | C# | 1.152 | 1.676 | 0.228 | 18.0% | 5/5 |
| Collatz conjecture | AquariusLang | 1.288 | 1.637 | 0.141 | 10.0% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 1.253 | 3.939 | 1.118 | 56.1% | 5/5 |
| Collatz conjecture | Python | 47.312 | 58.914 | 4.934 | 9.3% | 5/5 |
| Collatz conjecture | Node.js | 4.753 | 6.451 | 0.740 | 13.3% | 5/5 |
| Collatz conjecture | C# | 1.401 | 1.466 | 0.026 | 1.8% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 49.04, Node.js 41.43, AquariusLang 37.65, Python 2.13 (higher is faster).**

Pairwise composite speed: C# is 2.04× as fast as AquariusLang (typed); C# is 2.41× as fast as Node.js; C# is 2.66× as fast as AquariusLang; C# is 46.92× as fast as Python; AquariusLang (typed) is 1.18× as fast as Node.js; AquariusLang (typed) is 1.30× as fast as AquariusLang; AquariusLang (typed) is 23.01× as fast as Python; Node.js is 1.10× as fast as AquariusLang; Node.js is 19.44× as fast as Python; AquariusLang is 17.67× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs Node.js | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 2.039× | 2.414× | 2.656× | 46.924× |
| 2 | AquariusLang (typed) | 49.04 | 0.490× | 1.000× | 1.184× | 1.303× | 23.013× |
| 3 | Node.js | 41.43 | 0.414× | 0.845× | 1.000× | 1.100× | 19.442× |
| 4 | AquariusLang | 37.65 | 0.377× | 0.768× | 0.909× | 1.000× | 17.668× |
| 5 | Python | 2.13 | 0.021× | 0.043× | 0.051× | 0.057× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 28 | 1.705 | 1.706 | 30.415 | 2.155 | 0.749 | 0.06× | 0.06× | 0.07× | 0.02× |
| Ackermann function | 6 | 0.557 | 0.712 | 13.994 | 0.471 | 0.141 | 0.04× | 0.05× | 0.03× | 0.01× |
| Sieve of Eratosthenes | 10000 | 0.086 | 0.039 | 0.539 | 0.124 | 0.019 | 0.16× | 0.07× | 0.23× | 0.04× |
| Quicksort | 2000 | 0.230 | 0.114 | 1.494 | 0.168 | 0.076 | 0.15× | 0.08× | 0.11× | 0.05× |
| Matrix multiplication | 45 | 0.243 | 0.134 | 7.777 | 0.239 | 0.065 | 0.03× | 0.02× | 0.03× | 0.01× |
| Mandelbrot set | 80 | 0.318 | 0.321 | 12.369 | 0.233 | 0.247 | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 8 | 0.291 | 0.202 | 4.646 | 0.157 | 0.119 | 0.06× | 0.04× | 0.03× | 0.03× |
| Binary trees | 12 | 2.797 | 2.032 | 8.609 | 0.828 | 0.451 | 0.32× | 0.24× | 0.10× | 0.05× |
| Spectral norm | 60 | 0.272 | 0.252 | 14.204 | 0.310 | 0.132 | 0.02× | 0.02× | 0.02× | 0.01× |
| Collatz conjecture | 10000 | 1.284 | 1.234 | 65.128 | 3.331 | 1.351 | 0.02× | 0.02× | 0.05× | 0.02× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 28 | 1.706 | 2.155 | 1.26× | AquariusLang (typed), 1.26× faster |
| Ackermann function | 6 | 0.712 | 0.471 | 0.66× | Node.js, 1.51× faster |
| Sieve of Eratosthenes | 10000 | 0.039 | 0.124 | 3.21× | AquariusLang (typed), 3.21× faster |
| Quicksort | 2000 | 0.114 | 0.168 | 1.47× | AquariusLang (typed), 1.47× faster |
| Matrix multiplication | 45 | 0.134 | 0.239 | 1.78× | AquariusLang (typed), 1.78× faster |
| Mandelbrot set | 80 | 0.321 | 0.233 | 0.73× | Node.js, 1.38× faster |
| N-Queens | 8 | 0.202 | 0.157 | 0.78× | Node.js, 1.29× faster |
| Binary trees | 12 | 2.032 | 0.828 | 0.41× | Node.js, 2.45× faster |
| Spectral norm | 60 | 0.252 | 0.310 | 1.23× | AquariusLang (typed), 1.23× faster |
| Collatz conjecture | 10000 | 1.234 | 3.331 | 2.70× | AquariusLang (typed), 2.70× faster |
| **Geometric mean** | | | | **1.18×** | AquariusLang (typed), 1.18× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 1.528 | 1.857 | 0.148 | 8.8% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 1.524 | 2.003 | 0.212 | 12.2% | 5/5 |
| Recursive Fibonacci | Python | 26.158 | 45.552 | 7.652 | 23.0% | 5/5 |
| Recursive Fibonacci | Node.js | 1.994 | 2.270 | 0.111 | 5.2% | 5/5 |
| Recursive Fibonacci | C# | 0.733 | 0.969 | 0.099 | 12.5% | 5/5 |
| Ackermann function | AquariusLang | 0.555 | 0.733 | 0.092 | 14.8% | 5/5 |
| Ackermann function | AquariusLang (typed) | 0.545 | 0.748 | 0.094 | 14.3% | 5/5 |
| Ackermann function | Python | 10.973 | 17.812 | 2.862 | 20.6% | 5/5 |
| Ackermann function | Node.js | 0.358 | 0.491 | 0.063 | 14.5% | 5/5 |
| Ackermann function | C# | 0.128 | 0.195 | 0.027 | 18.3% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 0.082 | 0.106 | 0.010 | 10.9% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.038 | 0.051 | 0.007 | 15.2% | 5/5 |
| Sieve of Eratosthenes | Python | 0.528 | 0.721 | 0.081 | 14.1% | 5/5 |
| Sieve of Eratosthenes | Node.js | 0.117 | 0.181 | 0.027 | 19.6% | 5/5 |
| Sieve of Eratosthenes | C# | 0.019 | 0.031 | 0.005 | 24.4% | 5/5 |
| Quicksort | AquariusLang | 0.227 | 0.443 | 0.096 | 35.1% | 5/5 |
| Quicksort | AquariusLang (typed) | 0.111 | 0.154 | 0.018 | 14.5% | 5/5 |
| Quicksort | Python | 1.261 | 1.929 | 0.271 | 17.9% | 5/5 |
| Quicksort | Node.js | 0.150 | 0.190 | 0.015 | 8.8% | 5/5 |
| Quicksort | C# | 0.073 | 0.111 | 0.017 | 19.8% | 5/5 |
| Matrix multiplication | AquariusLang | 0.193 | 0.264 | 0.029 | 12.3% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 0.129 | 0.172 | 0.018 | 12.3% | 5/5 |
| Matrix multiplication | Python | 7.339 | 8.952 | 0.635 | 8.0% | 5/5 |
| Matrix multiplication | Node.js | 0.122 | 0.323 | 0.081 | 36.5% | 5/5 |
| Matrix multiplication | C# | 0.058 | 0.075 | 0.007 | 10.1% | 5/5 |
| Mandelbrot set | AquariusLang | 0.300 | 0.400 | 0.041 | 12.5% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 0.299 | 0.397 | 0.040 | 12.1% | 5/5 |
| Mandelbrot set | Python | 9.653 | 19.111 | 3.918 | 30.2% | 5/5 |
| Mandelbrot set | Node.js | 0.227 | 0.237 | 0.004 | 1.6% | 5/5 |
| Mandelbrot set | C# | 0.226 | 0.297 | 0.034 | 13.2% | 5/5 |
| N-Queens | AquariusLang | 0.286 | 0.332 | 0.019 | 6.2% | 5/5 |
| N-Queens | AquariusLang (typed) | 0.186 | 0.267 | 0.037 | 17.0% | 5/5 |
| N-Queens | Python | 3.760 | 11.342 | 3.181 | 55.6% | 5/5 |
| N-Queens | Node.js | 0.157 | 0.198 | 0.018 | 10.7% | 5/5 |
| N-Queens | C# | 0.112 | 0.166 | 0.023 | 17.8% | 5/5 |
| Binary trees | AquariusLang | 2.306 | 3.320 | 0.367 | 13.0% | 5/5 |
| Binary trees | AquariusLang (typed) | 1.677 | 2.714 | 0.438 | 20.5% | 5/5 |
| Binary trees | Python | 7.880 | 24.511 | 7.203 | 61.7% | 5/5 |
| Binary trees | Node.js | 0.765 | 0.866 | 0.040 | 4.9% | 5/5 |
| Binary trees | C# | 0.448 | 0.575 | 0.064 | 12.9% | 5/5 |
| Spectral norm | AquariusLang | 0.266 | 0.310 | 0.018 | 6.5% | 5/5 |
| Spectral norm | AquariusLang (typed) | 0.245 | 0.332 | 0.037 | 13.7% | 5/5 |
| Spectral norm | Python | 13.799 | 27.926 | 6.065 | 35.3% | 5/5 |
| Spectral norm | Node.js | 0.248 | 0.324 | 0.037 | 12.8% | 5/5 |
| Spectral norm | C# | 0.129 | 0.138 | 0.004 | 2.7% | 5/5 |
| Collatz conjecture | AquariusLang | 1.250 | 1.647 | 0.196 | 13.9% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 1.221 | 1.694 | 0.204 | 15.3% | 5/5 |
| Collatz conjecture | Python | 45.843 | 67.460 | 8.791 | 14.5% | 5/5 |
| Collatz conjecture | Node.js | 3.314 | 5.058 | 0.895 | 22.5% | 5/5 |
| Collatz conjecture | C# | 1.321 | 1.777 | 0.205 | 13.9% | 5/5 |

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

- Started: 2026-10-28T19:57:29.802469+08:00
- Finished: 2026-10-28T19:59:37.960873+08:00
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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261028-195729-802469\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261028-195729-802469\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261028-195729-802469\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

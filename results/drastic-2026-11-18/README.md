# Desktop performance benchmark: AquariusLang, AquariusLang (typed), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: C# 100.00, AquariusLang (typed) 63.49, AquariusLang 45.15, Node.js 36.49, Python 2.71
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 54.72, Node.js 47.35, AquariusLang 41.01, Python 2.22

The project provides ten classic algorithms, 50 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: C# 100.00, AquariusLang (typed) 63.49, AquariusLang 45.15, Node.js 36.49, Python 2.71 (higher is faster).**

Pairwise composite speed: C# is 1.57× as fast as AquariusLang (typed); C# is 2.21× as fast as AquariusLang; C# is 2.74× as fast as Node.js; C# is 36.90× as fast as Python; AquariusLang (typed) is 1.41× as fast as AquariusLang; AquariusLang (typed) is 1.74× as fast as Node.js; AquariusLang (typed) is 23.43× as fast as Python; AquariusLang is 1.24× as fast as Node.js; AquariusLang is 16.66× as fast as Python; Node.js is 13.47× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.575× | 2.215× | 2.740× | 36.903× |
| 2 | AquariusLang (typed) | 63.49 | 0.635× | 1.000× | 1.406× | 1.740× | 23.431× |
| 3 | AquariusLang | 45.15 | 0.452× | 0.711× | 1.000× | 1.237× | 16.662× |
| 4 | Node.js | 36.49 | 0.365× | 0.575× | 0.808× | 1.000× | 13.466× |
| 5 | Python | 2.71 | 0.027× | 0.043× | 0.060× | 0.074× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 14.007 | 13.733 | 213.311 | 16.103 | 5.958 | 0.07× | 0.06× | 0.08× | 0.03× |
| Ackermann function | 8 | 11.471 | 8.539 | 229.193 | 7.788 | 2.389 | 0.05× | 0.04× | 0.03× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.908 | 0.958 | 13.719 | 6.460 | 0.900 | 0.14× | 0.07× | 0.47× | 0.07× |
| Quicksort | 30000 | 5.271 | 2.785 | 29.004 | 6.812 | 2.270 | 0.18× | 0.10× | 0.23× | 0.08× |
| Matrix multiplication | 150 | 8.104 | 2.548 | 218.574 | 12.155 | 2.407 | 0.04× | 0.01× | 0.06× | 0.01× |
| Mandelbrot set | 300 | 6.067 | 4.935 | 154.541 | 5.959 | 4.114 | 0.04× | 0.03× | 0.04× | 0.03× |
| N-Queens | 10 | 6.707 | 5.890 | 114.573 | 4.987 | 3.773 | 0.06× | 0.05× | 0.04× | 0.03× |
| Binary trees | 16 | 59.046 | 54.954 | 389.660 | 30.754 | 17.998 | 0.15× | 0.14× | 0.08× | 0.05× |
| Spectral norm | 250 | 6.732 | 3.728 | 324.703 | 10.601 | 3.306 | 0.02× | 0.01× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 17.600 | 25.993 | 645.845 | 48.259 | 20.307 | 0.03× | 0.04× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 13.733 | 16.103 | 1.17× | AquariusLang (typed), 1.17× faster |
| Ackermann function | 8 | 8.539 | 7.788 | 0.91× | Node.js, 1.10× faster |
| Sieve of Eratosthenes | 200000 | 0.958 | 6.460 | 6.75× | AquariusLang (typed), 6.75× faster |
| Quicksort | 30000 | 2.785 | 6.812 | 2.45× | AquariusLang (typed), 2.45× faster |
| Matrix multiplication | 150 | 2.548 | 12.155 | 4.77× | AquariusLang (typed), 4.77× faster |
| Mandelbrot set | 300 | 4.935 | 5.959 | 1.21× | AquariusLang (typed), 1.21× faster |
| N-Queens | 10 | 5.890 | 4.987 | 0.85× | Node.js, 1.18× faster |
| Binary trees | 16 | 54.954 | 30.754 | 0.56× | Node.js, 1.79× faster |
| Spectral norm | 250 | 3.728 | 10.601 | 2.84× | AquariusLang (typed), 2.84× faster |
| Collatz conjecture | 100000 | 25.993 | 48.259 | 1.86× | AquariusLang (typed), 1.86× faster |
| **Geometric mean** | | | | **1.74×** | AquariusLang (typed), 1.74× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 11.381 | 15.847 | 2.033 | 14.8% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 11.987 | 14.092 | 0.875 | 6.5% | 5/5 |
| Recursive Fibonacci | Python | 192.003 | 227.319 | 13.975 | 6.6% | 5/5 |
| Recursive Fibonacci | Node.js | 13.509 | 17.174 | 1.549 | 10.0% | 5/5 |
| Recursive Fibonacci | C# | 5.476 | 9.166 | 1.504 | 23.1% | 5/5 |
| Ackermann function | AquariusLang | 9.511 | 11.839 | 0.932 | 8.4% | 5/5 |
| Ackermann function | AquariusLang (typed) | 7.950 | 9.648 | 0.682 | 8.0% | 5/5 |
| Ackermann function | Python | 202.869 | 403.740 | 83.639 | 31.3% | 5/5 |
| Ackermann function | Node.js | 7.439 | 8.405 | 0.387 | 5.0% | 5/5 |
| Ackermann function | C# | 2.234 | 3.201 | 0.397 | 15.3% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.598 | 2.054 | 0.209 | 11.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.954 | 1.013 | 0.025 | 2.6% | 5/5 |
| Sieve of Eratosthenes | Python | 12.657 | 15.010 | 0.922 | 6.8% | 5/5 |
| Sieve of Eratosthenes | Node.js | 5.380 | 9.622 | 1.747 | 25.3% | 5/5 |
| Sieve of Eratosthenes | C# | 0.835 | 0.984 | 0.065 | 7.1% | 5/5 |
| Quicksort | AquariusLang | 4.356 | 5.489 | 0.534 | 10.6% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.219 | 3.296 | 0.382 | 13.7% | 5/5 |
| Quicksort | Python | 26.616 | 35.260 | 3.312 | 11.0% | 5/5 |
| Quicksort | Node.js | 6.271 | 8.265 | 0.964 | 13.4% | 5/5 |
| Quicksort | C# | 2.141 | 2.912 | 0.343 | 14.2% | 5/5 |
| Matrix multiplication | AquariusLang | 6.690 | 9.310 | 0.973 | 12.3% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.349 | 2.987 | 0.256 | 9.8% | 5/5 |
| Matrix multiplication | Python | 207.853 | 237.200 | 12.085 | 5.5% | 5/5 |
| Matrix multiplication | Node.js | 9.265 | 12.637 | 1.518 | 13.3% | 5/5 |
| Matrix multiplication | C# | 2.045 | 2.718 | 0.294 | 12.4% | 5/5 |
| Mandelbrot set | AquariusLang | 5.195 | 6.571 | 0.516 | 8.5% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.365 | 6.634 | 1.000 | 18.6% | 5/5 |
| Mandelbrot set | Python | 141.093 | 176.171 | 12.783 | 8.2% | 5/5 |
| Mandelbrot set | Node.js | 5.277 | 6.850 | 0.598 | 10.0% | 5/5 |
| Mandelbrot set | C# | 3.578 | 5.723 | 0.855 | 19.4% | 5/5 |
| N-Queens | AquariusLang | 5.773 | 9.038 | 1.211 | 17.3% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.294 | 6.475 | 0.914 | 16.6% | 5/5 |
| N-Queens | Python | 100.920 | 138.573 | 14.328 | 12.2% | 5/5 |
| N-Queens | Node.js | 4.440 | 5.034 | 0.248 | 5.1% | 5/5 |
| N-Queens | C# | 3.139 | 4.056 | 0.374 | 10.0% | 5/5 |
| Binary trees | AquariusLang | 56.267 | 80.923 | 10.339 | 16.4% | 5/5 |
| Binary trees | AquariusLang (typed) | 53.642 | 58.763 | 2.152 | 3.9% | 5/5 |
| Binary trees | Python | 307.195 | 414.288 | 42.974 | 11.6% | 5/5 |
| Binary trees | Node.js | 28.321 | 32.690 | 2.009 | 6.6% | 5/5 |
| Binary trees | C# | 17.645 | 20.109 | 1.001 | 5.4% | 5/5 |
| Spectral norm | AquariusLang | 5.516 | 7.166 | 0.666 | 10.2% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.500 | 4.532 | 0.411 | 10.5% | 5/5 |
| Spectral norm | Python | 273.022 | 335.877 | 25.542 | 8.1% | 5/5 |
| Spectral norm | Node.js | 8.751 | 14.752 | 2.207 | 19.9% | 5/5 |
| Spectral norm | C# | 3.125 | 4.095 | 0.424 | 12.0% | 5/5 |
| Collatz conjecture | AquariusLang | 15.658 | 19.789 | 1.570 | 8.8% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 20.233 | 27.191 | 2.969 | 12.0% | 5/5 |
| Collatz conjecture | Python | 601.298 | 715.535 | 42.483 | 6.5% | 5/5 |
| Collatz conjecture | Node.js | 44.789 | 50.414 | 2.304 | 4.8% | 5/5 |
| Collatz conjecture | C# | 17.413 | 26.652 | 3.561 | 16.5% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 54.72, Node.js 47.35, AquariusLang 41.01, Python 2.22 (higher is faster).**

Pairwise composite speed: C# is 1.83× as fast as AquariusLang (typed); C# is 2.11× as fast as Node.js; C# is 2.44× as fast as AquariusLang; C# is 45.09× as fast as Python; AquariusLang (typed) is 1.16× as fast as Node.js; AquariusLang (typed) is 1.33× as fast as AquariusLang; AquariusLang (typed) is 24.67× as fast as Python; Node.js is 1.15× as fast as AquariusLang; Node.js is 21.35× as fast as Python; AquariusLang is 18.49× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs Node.js | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.828× | 2.112× | 2.438× | 45.086× |
| 2 | AquariusLang (typed) | 54.72 | 0.547× | 1.000× | 1.156× | 1.334× | 24.670× |
| 3 | Node.js | 47.35 | 0.473× | 0.865× | 1.000× | 1.155× | 21.347× |
| 4 | AquariusLang | 41.01 | 0.410× | 0.749× | 0.866× | 1.000× | 18.489× |
| 5 | Python | 2.22 | 0.022× | 0.041× | 0.047× | 0.054× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 11.669 | 11.124 | 222.282 | 14.349 | 5.480 | 0.05× | 0.05× | 0.06× | 0.02× |
| Ackermann function | 8 | 8.951 | 8.503 | 220.003 | 8.917 | 2.296 | 0.04× | 0.04× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.599 | 1.012 | 14.454 | 2.413 | 0.402 | 0.11× | 0.07× | 0.17× | 0.03× |
| Quicksort | 30000 | 5.196 | 2.748 | 28.160 | 3.191 | 1.897 | 0.18× | 0.10× | 0.11× | 0.07× |
| Matrix multiplication | 150 | 6.902 | 2.693 | 237.534 | 3.510 | 1.979 | 0.03× | 0.01× | 0.01× | 0.01× |
| Mandelbrot set | 300 | 5.271 | 4.825 | 148.325 | 3.735 | 3.291 | 0.04× | 0.03× | 0.03× | 0.02× |
| N-Queens | 10 | 6.949 | 4.695 | 109.988 | 4.253 | 3.249 | 0.06× | 0.04× | 0.04× | 0.03× |
| Binary trees | 16 | 52.956 | 51.157 | 373.461 | 14.540 | 16.831 | 0.14× | 0.14× | 0.04× | 0.05× |
| Spectral norm | 250 | 5.625 | 4.603 | 291.886 | 7.617 | 2.386 | 0.02× | 0.02× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 18.929 | 18.315 | 687.001 | 48.322 | 20.441 | 0.03× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 11.124 | 14.349 | 1.29× | AquariusLang (typed), 1.29× faster |
| Ackermann function | 8 | 8.503 | 8.917 | 1.05× | AquariusLang (typed), 1.05× faster |
| Sieve of Eratosthenes | 200000 | 1.012 | 2.413 | 2.38× | AquariusLang (typed), 2.38× faster |
| Quicksort | 30000 | 2.748 | 3.191 | 1.16× | AquariusLang (typed), 1.16× faster |
| Matrix multiplication | 150 | 2.693 | 3.510 | 1.30× | AquariusLang (typed), 1.30× faster |
| Mandelbrot set | 300 | 4.825 | 3.735 | 0.77× | Node.js, 1.29× faster |
| N-Queens | 10 | 4.695 | 4.253 | 0.91× | Node.js, 1.10× faster |
| Binary trees | 16 | 51.157 | 14.540 | 0.28× | Node.js, 3.52× faster |
| Spectral norm | 250 | 4.603 | 7.617 | 1.65× | AquariusLang (typed), 1.65× faster |
| Collatz conjecture | 100000 | 18.315 | 48.322 | 2.64× | AquariusLang (typed), 2.64× faster |
| **Geometric mean** | | | | **1.16×** | AquariusLang (typed), 1.16× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 10.195 | 13.452 | 1.377 | 11.9% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 10.441 | 12.870 | 1.118 | 9.7% | 5/5 |
| Recursive Fibonacci | Python | 202.456 | 278.554 | 30.389 | 13.2% | 5/5 |
| Recursive Fibonacci | Node.js | 14.014 | 15.958 | 0.766 | 5.2% | 5/5 |
| Recursive Fibonacci | C# | 5.361 | 6.191 | 0.397 | 6.9% | 5/5 |
| Ackermann function | AquariusLang | 7.810 | 11.232 | 1.257 | 13.6% | 5/5 |
| Ackermann function | AquariusLang (typed) | 6.952 | 9.111 | 0.918 | 11.1% | 5/5 |
| Ackermann function | Python | 199.107 | 275.694 | 29.003 | 12.6% | 5/5 |
| Ackermann function | Node.js | 7.085 | 14.672 | 2.932 | 30.4% | 5/5 |
| Ackermann function | C# | 2.228 | 2.896 | 0.279 | 11.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.334 | 1.948 | 0.219 | 13.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.719 | 1.232 | 0.231 | 23.0% | 5/5 |
| Sieve of Eratosthenes | Python | 12.737 | 17.262 | 1.944 | 13.0% | 5/5 |
| Sieve of Eratosthenes | Node.js | 2.326 | 2.892 | 0.259 | 10.1% | 5/5 |
| Sieve of Eratosthenes | C# | 0.384 | 0.450 | 0.030 | 7.2% | 5/5 |
| Quicksort | AquariusLang | 4.419 | 6.005 | 0.605 | 11.7% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.617 | 4.502 | 0.797 | 25.8% | 5/5 |
| Quicksort | Python | 26.814 | 31.816 | 2.391 | 8.2% | 5/5 |
| Quicksort | Node.js | 2.927 | 3.360 | 0.158 | 5.0% | 5/5 |
| Quicksort | C# | 1.629 | 2.319 | 0.290 | 15.0% | 5/5 |
| Matrix multiplication | AquariusLang | 6.434 | 7.580 | 0.481 | 6.9% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.313 | 2.979 | 0.286 | 10.7% | 5/5 |
| Matrix multiplication | Python | 210.535 | 270.542 | 22.618 | 9.4% | 5/5 |
| Matrix multiplication | Node.js | 3.305 | 4.145 | 0.343 | 9.5% | 5/5 |
| Matrix multiplication | C# | 1.905 | 2.216 | 0.125 | 6.3% | 5/5 |
| Mandelbrot set | AquariusLang | 4.712 | 5.684 | 0.391 | 7.4% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 4.124 | 5.806 | 0.687 | 13.8% | 5/5 |
| Mandelbrot set | Python | 141.822 | 159.570 | 6.655 | 4.4% | 5/5 |
| Mandelbrot set | Node.js | 3.173 | 4.300 | 0.402 | 10.8% | 5/5 |
| Mandelbrot set | C# | 3.155 | 4.499 | 0.560 | 15.9% | 5/5 |
| N-Queens | AquariusLang | 6.081 | 7.962 | 0.682 | 9.8% | 5/5 |
| N-Queens | AquariusLang (typed) | 4.001 | 5.347 | 0.507 | 10.6% | 5/5 |
| N-Queens | Python | 97.203 | 115.449 | 7.380 | 6.9% | 5/5 |
| N-Queens | Node.js | 3.890 | 4.840 | 0.355 | 8.3% | 5/5 |
| N-Queens | C# | 2.844 | 3.484 | 0.231 | 7.2% | 5/5 |
| Binary trees | AquariusLang | 38.411 | 62.237 | 8.914 | 17.4% | 5/5 |
| Binary trees | AquariusLang (typed) | 44.992 | 62.736 | 7.089 | 13.8% | 5/5 |
| Binary trees | Python | 327.671 | 423.808 | 37.240 | 9.9% | 5/5 |
| Binary trees | Node.js | 14.097 | 17.104 | 1.291 | 8.5% | 5/5 |
| Binary trees | C# | 15.552 | 19.446 | 1.424 | 8.3% | 5/5 |
| Spectral norm | AquariusLang | 4.853 | 6.068 | 0.533 | 9.7% | 5/5 |
| Spectral norm | AquariusLang (typed) | 3.563 | 4.880 | 0.597 | 13.9% | 5/5 |
| Spectral norm | Python | 272.591 | 332.198 | 27.032 | 9.0% | 5/5 |
| Spectral norm | Node.js | 6.872 | 8.148 | 0.552 | 7.4% | 5/5 |
| Spectral norm | C# | 2.050 | 2.475 | 0.184 | 8.0% | 5/5 |
| Collatz conjecture | AquariusLang | 15.635 | 19.925 | 1.755 | 9.4% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 17.945 | 20.155 | 0.972 | 5.2% | 5/5 |
| Collatz conjecture | Python | 600.373 | 713.950 | 47.957 | 7.2% | 5/5 |
| Collatz conjecture | Node.js | 44.740 | 57.280 | 5.040 | 10.1% | 5/5 |
| Collatz conjecture | C# | 17.592 | 22.383 | 1.813 | 9.0% | 5/5 |

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

- Started: 2026-11-18T11:04:47.282021+08:00
- Finished: 2026-11-18T11:10:08.033613+08:00
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
| AquariusLang | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua\aqua.exe |
| AquariusLang (typed) | no version option; identified by release folder and binary hashes | C:\OfficialProjects\AquariusLangTW\dist\aqua\aqua.exe |
| Python | Python 3.12.10 | C:\Users\templ\.pyenv\pyenv-win\versions\3.12.10\python.exe |
| Node.js | v24.18.0 | C:\Program Files\nodejs\node.exe |
| C# | SDKs: 8.0.426 [C:\Program Files\dotnet\sdk] Runtimes: Microsoft.AspNetCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App] Microsoft.NETCore.App 6.0.36 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.NETCore.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.NETCore.App] Microsoft.WindowsDesktop.App 8.0.19 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] Microsoft.WindowsDesktop.App 8.0.32 [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App] | C:\Program Files\dotnet\dotnet.exe |

AquariusLang release folder: `C:\OfficialProjects\AquariusLangTW\dist\aqua`.

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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\drastic-2026-11-18\20261118-110447-282021\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\drastic-2026-11-18\20261118-110447-282021\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\drastic-2026-11-18\20261118-110447-282021\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

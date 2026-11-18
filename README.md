# Desktop performance benchmark: AquariusLang, AquariusLang (typed), AquariusLang (Native AOT compiler), AquariusLang (typed, Native AOT compiler), Python, Node.js, C#

<p><a href="README.tw.md">繁體中文</a> | <strong>English</strong></p>

This run measured 2 modes, each with its own composite score (higher is faster; the fastest language scores 100):

- **Standard mode (cold start, one timed run per process)**: C# 100.00, AquariusLang (typed, Native AOT compiler) 67.11, AquariusLang (typed) 66.52, AquariusLang (Native AOT compiler) 49.78, AquariusLang 49.15, Node.js 36.77, Python 2.61
- **Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)**: C# 100.00, AquariusLang (typed) 57.49, AquariusLang (typed, Native AOT compiler) 55.92, Node.js 46.78, AquariusLang (Native AOT compiler) 44.24, AquariusLang 43.95, Python 2.20

The project provides ten classic algorithms, 112 standalone benchmark programs, and a Python harness that validates the results and generates the READMEs and the JSON and CSV reports.

## Standard mode (cold start, one timed run per process)

Each process runs and times the workload once, with no in-process warm-up, as in the original design. The JIT compilation and optimization of C# and Node.js fall inside the timed interval, while Wasmtime has already compiled the AquariusLang Wasm before timing starts, so this mode reflects a short program's first run after process start. Each value is the median of 5 process timings.

**Composite performance: C# 100.00, AquariusLang (typed, Native AOT compiler) 67.11, AquariusLang (typed) 66.52, AquariusLang (Native AOT compiler) 49.78, AquariusLang 49.15, Node.js 36.77, Python 2.61 (higher is faster).**

Pairwise composite speed: C# is 1.49× as fast as AquariusLang (typed, Native AOT compiler); C# is 1.50× as fast as AquariusLang (typed); C# is 2.01× as fast as AquariusLang (Native AOT compiler); C# is 2.03× as fast as AquariusLang; C# is 2.72× as fast as Node.js; C# is 38.30× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.01× as fast as AquariusLang (typed); AquariusLang (typed, Native AOT compiler) is 1.35× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 1.37× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 1.83× as fast as Node.js; AquariusLang (typed, Native AOT compiler) is 25.71× as fast as Python; AquariusLang (typed) is 1.34× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 1.35× as fast as AquariusLang; AquariusLang (typed) is 1.81× as fast as Node.js; AquariusLang (typed) is 25.48× as fast as Python; AquariusLang (Native AOT compiler) is 1.01× as fast as AquariusLang; AquariusLang (Native AOT compiler) is 1.35× as fast as Node.js; AquariusLang (Native AOT compiler) is 19.07× as fast as Python; AquariusLang is 1.34× as fast as Node.js; AquariusLang is 18.83× as fast as Python; Node.js is 14.08× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs AquariusLang (typed) | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang | Speed vs Node.js | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.490× | 1.503× | 2.009× | 2.034× | 2.719× | 38.301× |
| 2 | AquariusLang (typed, Native AOT compiler) | 67.11 | 0.671× | 1.000× | 1.009× | 1.348× | 1.365× | 1.825× | 25.706× |
| 3 | AquariusLang (typed) | 66.52 | 0.665× | 0.991× | 1.000× | 1.336× | 1.353× | 1.809× | 25.478× |
| 4 | AquariusLang (Native AOT compiler) | 49.78 | 0.498× | 0.742× | 0.748× | 1.000× | 1.013× | 1.354× | 19.066× |
| 5 | AquariusLang | 49.15 | 0.492× | 0.732× | 0.739× | 0.987× | 1.000× | 1.337× | 18.827× |
| 6 | Node.js | 36.77 | 0.368× | 0.548× | 0.553× | 0.739× | 0.748× | 1.000× | 14.084× |
| 7 | Python | 2.61 | 0.026× | 0.039× | 0.039× | 0.052× | 0.053× | 0.071× | 1.000× |

### Results per benchmark (standard mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 14.622 | 16.237 | 15.039 | 14.780 | 262.839 | 18.248 | 7.104 | 0.06× | 0.06× | 0.06× | 0.06× | 0.07× | 0.03× |
| Ackermann function | 8 | 12.272 | 11.096 | 10.954 | 11.524 | 277.475 | 10.822 | 2.869 | 0.04× | 0.04× | 0.04× | 0.04× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 2.159 | 0.930 | 1.895 | 0.941 | 16.911 | 7.631 | 1.049 | 0.13× | 0.06× | 0.11× | 0.06× | 0.45× | 0.06× |
| Quicksort | 30000 | 6.048 | 3.380 | 6.064 | 2.976 | 39.146 | 7.972 | 2.965 | 0.15× | 0.09× | 0.15× | 0.08× | 0.20× | 0.08× |
| Matrix multiplication | 150 | 8.421 | 3.211 | 7.858 | 3.441 | 287.791 | 12.466 | 2.786 | 0.03× | 0.01× | 0.03× | 0.01× | 0.04× | 0.01× |
| Mandelbrot set | 300 | 6.455 | 6.204 | 6.646 | 6.328 | 202.454 | 7.330 | 4.546 | 0.03× | 0.03× | 0.03× | 0.03× | 0.04× | 0.02× |
| N-Queens | 10 | 8.477 | 5.607 | 8.679 | 5.817 | 137.904 | 6.364 | 4.503 | 0.06× | 0.04× | 0.06× | 0.04× | 0.05× | 0.03× |
| Binary trees | 16 | 67.347 | 73.082 | 73.269 | 64.943 | 509.740 | 34.341 | 23.461 | 0.13× | 0.14× | 0.14× | 0.13× | 0.07× | 0.05× |
| Spectral norm | 250 | 6.597 | 5.055 | 6.687 | 5.159 | 367.786 | 13.034 | 4.511 | 0.02× | 0.01× | 0.02× | 0.01× | 0.04× | 0.01× |
| Collatz conjecture | 100000 | 23.412 | 23.323 | 23.545 | 24.642 | 863.712 | 65.406 | 24.166 | 0.03× | 0.03× | 0.03× | 0.03× | 0.08× | 0.03× |

### AquariusLang (typed) vs Node.js (standard mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 16.237 | 18.248 | 1.12× | AquariusLang (typed), 1.12× faster |
| Ackermann function | 8 | 11.096 | 10.822 | 0.98× | Node.js, 1.03× faster |
| Sieve of Eratosthenes | 200000 | 0.930 | 7.631 | 8.20× | AquariusLang (typed), 8.20× faster |
| Quicksort | 30000 | 3.380 | 7.972 | 2.36× | AquariusLang (typed), 2.36× faster |
| Matrix multiplication | 150 | 3.211 | 12.466 | 3.88× | AquariusLang (typed), 3.88× faster |
| Mandelbrot set | 300 | 6.204 | 7.330 | 1.18× | AquariusLang (typed), 1.18× faster |
| N-Queens | 10 | 5.607 | 6.364 | 1.13× | AquariusLang (typed), 1.13× faster |
| Binary trees | 16 | 73.082 | 34.341 | 0.47× | Node.js, 2.13× faster |
| Spectral norm | 250 | 5.055 | 13.034 | 2.58× | AquariusLang (typed), 2.58× faster |
| Collatz conjecture | 100000 | 23.323 | 65.406 | 2.80× | AquariusLang (typed), 2.80× faster |
| **Geometric mean** | | | | **1.81×** | AquariusLang (typed), 1.81× faster |

### Timing variability (standard mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 12.263 | 20.219 | 2.971 | 19.2% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 14.666 | 17.685 | 1.282 | 7.8% | 5/5 |
| Recursive Fibonacci | AquariusLang (Native AOT compiler) | 12.397 | 16.754 | 1.631 | 11.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed, Native AOT compiler) | 12.999 | 15.515 | 0.936 | 6.5% | 5/5 |
| Recursive Fibonacci | Python | 210.782 | 269.114 | 23.824 | 9.4% | 5/5 |
| Recursive Fibonacci | Node.js | 16.552 | 20.154 | 1.446 | 8.0% | 5/5 |
| Recursive Fibonacci | C# | 6.313 | 7.759 | 0.537 | 7.5% | 5/5 |
| Ackermann function | AquariusLang | 11.809 | 13.230 | 0.528 | 4.2% | 5/5 |
| Ackermann function | AquariusLang (typed) | 9.848 | 13.364 | 1.273 | 11.3% | 5/5 |
| Ackermann function | AquariusLang (Native AOT compiler) | 9.197 | 13.004 | 1.463 | 13.0% | 5/5 |
| Ackermann function | AquariusLang (typed, Native AOT compiler) | 9.133 | 12.351 | 1.295 | 11.8% | 5/5 |
| Ackermann function | Python | 235.870 | 332.379 | 39.566 | 13.7% | 5/5 |
| Ackermann function | Node.js | 9.412 | 11.421 | 0.806 | 7.5% | 5/5 |
| Ackermann function | C# | 2.857 | 3.318 | 0.202 | 6.7% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.965 | 2.196 | 0.093 | 4.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.878 | 1.125 | 0.112 | 11.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (Native AOT compiler) | 1.822 | 2.298 | 0.193 | 9.8% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed, Native AOT compiler) | 0.744 | 1.176 | 0.157 | 16.4% | 5/5 |
| Sieve of Eratosthenes | Python | 13.768 | 18.423 | 1.859 | 11.4% | 5/5 |
| Sieve of Eratosthenes | Node.js | 5.789 | 8.785 | 1.095 | 14.8% | 5/5 |
| Sieve of Eratosthenes | C# | 0.994 | 1.059 | 0.027 | 2.6% | 5/5 |
| Quicksort | AquariusLang | 5.230 | 6.275 | 0.431 | 7.4% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.891 | 3.596 | 0.292 | 8.9% | 5/5 |
| Quicksort | AquariusLang (Native AOT compiler) | 4.998 | 7.157 | 0.806 | 13.2% | 5/5 |
| Quicksort | AquariusLang (typed, Native AOT compiler) | 2.642 | 3.381 | 0.263 | 8.8% | 5/5 |
| Quicksort | Python | 27.539 | 43.311 | 6.804 | 18.3% | 5/5 |
| Quicksort | Node.js | 7.425 | 8.167 | 0.283 | 3.6% | 5/5 |
| Quicksort | C# | 2.663 | 3.355 | 0.273 | 9.0% | 5/5 |
| Matrix multiplication | AquariusLang | 7.748 | 8.823 | 0.421 | 5.1% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 3.067 | 6.616 | 1.526 | 39.2% | 5/5 |
| Matrix multiplication | AquariusLang (Native AOT compiler) | 6.395 | 9.338 | 1.072 | 13.5% | 5/5 |
| Matrix multiplication | AquariusLang (typed, Native AOT compiler) | 3.107 | 4.191 | 0.445 | 12.5% | 5/5 |
| Matrix multiplication | Python | 235.661 | 310.099 | 35.887 | 13.0% | 5/5 |
| Matrix multiplication | Node.js | 9.412 | 12.881 | 1.728 | 15.2% | 5/5 |
| Matrix multiplication | C# | 2.492 | 3.240 | 0.285 | 10.2% | 5/5 |
| Mandelbrot set | AquariusLang | 6.235 | 7.447 | 0.530 | 7.9% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 5.685 | 7.248 | 0.591 | 9.2% | 5/5 |
| Mandelbrot set | AquariusLang (Native AOT compiler) | 6.344 | 6.799 | 0.173 | 2.6% | 5/5 |
| Mandelbrot set | AquariusLang (typed, Native AOT compiler) | 6.073 | 7.088 | 0.495 | 7.6% | 5/5 |
| Mandelbrot set | Python | 169.607 | 232.037 | 22.851 | 11.3% | 5/5 |
| Mandelbrot set | Node.js | 5.974 | 7.989 | 0.763 | 10.5% | 5/5 |
| Mandelbrot set | C# | 3.817 | 4.923 | 0.433 | 9.6% | 5/5 |
| N-Queens | AquariusLang | 7.647 | 8.855 | 0.466 | 5.5% | 5/5 |
| N-Queens | AquariusLang (typed) | 5.090 | 6.238 | 0.430 | 7.7% | 5/5 |
| N-Queens | AquariusLang (Native AOT compiler) | 7.230 | 9.178 | 0.732 | 8.6% | 5/5 |
| N-Queens | AquariusLang (typed, Native AOT compiler) | 4.421 | 5.967 | 0.651 | 11.7% | 5/5 |
| N-Queens | Python | 108.593 | 159.466 | 18.174 | 13.3% | 5/5 |
| N-Queens | Node.js | 4.612 | 6.834 | 0.875 | 14.3% | 5/5 |
| N-Queens | C# | 3.371 | 5.450 | 0.745 | 16.6% | 5/5 |
| Binary trees | AquariusLang | 59.663 | 76.259 | 7.352 | 10.9% | 5/5 |
| Binary trees | AquariusLang (typed) | 52.044 | 82.182 | 11.314 | 16.3% | 5/5 |
| Binary trees | AquariusLang (Native AOT compiler) | 67.614 | 74.157 | 2.679 | 3.7% | 5/5 |
| Binary trees | AquariusLang (typed, Native AOT compiler) | 58.946 | 71.653 | 5.405 | 8.2% | 5/5 |
| Binary trees | Python | 445.102 | 568.270 | 46.905 | 9.1% | 5/5 |
| Binary trees | Node.js | 26.016 | 41.183 | 5.817 | 16.7% | 5/5 |
| Binary trees | C# | 21.036 | 26.215 | 1.843 | 7.8% | 5/5 |
| Spectral norm | AquariusLang | 5.410 | 7.449 | 0.729 | 11.2% | 5/5 |
| Spectral norm | AquariusLang (typed) | 4.530 | 6.476 | 0.785 | 14.5% | 5/5 |
| Spectral norm | AquariusLang (Native AOT compiler) | 6.263 | 7.289 | 0.392 | 5.8% | 5/5 |
| Spectral norm | AquariusLang (typed, Native AOT compiler) | 4.803 | 5.736 | 0.346 | 6.6% | 5/5 |
| Spectral norm | Python | 306.564 | 412.989 | 37.903 | 10.4% | 5/5 |
| Spectral norm | Node.js | 10.841 | 14.437 | 1.320 | 10.3% | 5/5 |
| Spectral norm | C# | 3.821 | 4.924 | 0.399 | 9.0% | 5/5 |
| Collatz conjecture | AquariusLang | 18.898 | 26.464 | 3.240 | 14.3% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 21.716 | 23.865 | 0.927 | 4.1% | 5/5 |
| Collatz conjecture | AquariusLang (Native AOT compiler) | 20.372 | 27.231 | 2.446 | 10.4% | 5/5 |
| Collatz conjecture | AquariusLang (typed, Native AOT compiler) | 21.620 | 27.474 | 2.241 | 9.1% | 5/5 |
| Collatz conjecture | Python | 720.942 | 998.240 | 98.749 | 11.5% | 5/5 |
| Collatz conjecture | Node.js | 60.674 | 88.085 | 10.990 | 16.0% | 5/5 |
| Collatz conjecture | C# | 21.558 | 26.301 | 1.943 | 8.2% | 5/5 |

## Warmed mode (5 in-process warm-up runs, then the median of 5 timed runs)

Each process first runs the same workload 5 times untimed in the same process so the JIT of C# and Node.js finishes optimizing before timing, then times 5 consecutive runs in the same process and takes their median as the process value; each value is the median of 5 process values. Every language gets the same warm-up and timed run counts.

**Composite performance: C# 100.00, AquariusLang (typed) 57.49, AquariusLang (typed, Native AOT compiler) 55.92, Node.js 46.78, AquariusLang (Native AOT compiler) 44.24, AquariusLang 43.95, Python 2.20 (higher is faster).**

Pairwise composite speed: C# is 1.74× as fast as AquariusLang (typed); C# is 1.79× as fast as AquariusLang (typed, Native AOT compiler); C# is 2.14× as fast as Node.js; C# is 2.26× as fast as AquariusLang (Native AOT compiler); C# is 2.28× as fast as AquariusLang; C# is 45.38× as fast as Python; AquariusLang (typed) is 1.03× as fast as AquariusLang (typed, Native AOT compiler); AquariusLang (typed) is 1.23× as fast as Node.js; AquariusLang (typed) is 1.30× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed) is 1.31× as fast as AquariusLang; AquariusLang (typed) is 26.09× as fast as Python; AquariusLang (typed, Native AOT compiler) is 1.20× as fast as Node.js; AquariusLang (typed, Native AOT compiler) is 1.26× as fast as AquariusLang (Native AOT compiler); AquariusLang (typed, Native AOT compiler) is 1.27× as fast as AquariusLang; AquariusLang (typed, Native AOT compiler) is 25.38× as fast as Python; Node.js is 1.06× as fast as AquariusLang (Native AOT compiler); Node.js is 1.06× as fast as AquariusLang; Node.js is 21.23× as fast as Python; AquariusLang (Native AOT compiler) is 1.01× as fast as AquariusLang; AquariusLang (Native AOT compiler) is 20.08× as fast as Python; AquariusLang is 19.94× as fast as Python.

| Rank | Language | Composite score | Speed vs C# | Speed vs AquariusLang (typed) | Speed vs AquariusLang (typed, Native AOT compiler) | Speed vs Node.js | Speed vs AquariusLang (Native AOT compiler) | Speed vs AquariusLang | Speed vs Python |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | C# | 100.00 | 1.000× | 1.740× | 1.788× | 2.138× | 2.260× | 2.276× | 45.383× |
| 2 | AquariusLang (typed) | 57.49 | 0.575× | 1.000× | 1.028× | 1.229× | 1.299× | 1.308× | 26.090× |
| 3 | AquariusLang (typed, Native AOT compiler) | 55.92 | 0.559× | 0.973× | 1.000× | 1.195× | 1.264× | 1.272× | 25.377× |
| 4 | Node.js | 46.78 | 0.468× | 0.814× | 0.837× | 1.000× | 1.057× | 1.065× | 21.231× |
| 5 | AquariusLang (Native AOT compiler) | 44.24 | 0.442× | 0.770× | 0.791× | 0.946× | 1.000× | 1.007× | 20.078× |
| 6 | AquariusLang | 43.95 | 0.439× | 0.764× | 0.786× | 0.939× | 0.993× | 1.000× | 19.944× |
| 7 | Python | 2.20 | 0.022× | 0.038× | 0.039× | 0.047× | 0.050× | 0.050× | 1.000× |

### Results per benchmark (warmed mode)

Times are in milliseconds (ms); lower is faster. Time ratio = the language's median time ÷ Python's median time; below 1 means that test ran faster than Python. This ratio points the opposite way from the composite score.

| Benchmark | n | AquariusLang median | AquariusLang (typed) median | AquariusLang (Native AOT compiler) median | AquariusLang (typed, Native AOT compiler) median | Python median | Node.js median | C# median | AquariusLang / Python time ratio | AquariusLang (typed) / Python time ratio | AquariusLang (Native AOT compiler) / Python time ratio | AquariusLang (typed, Native AOT compiler) / Python time ratio | Node.js / Python time ratio | C# / Python time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | 32 | 14.238 | 13.602 | 14.172 | 16.749 | 257.779 | 18.889 | 7.075 | 0.06× | 0.05× | 0.05× | 0.06× | 0.07× | 0.03× |
| Ackermann function | 8 | 10.685 | 11.099 | 10.583 | 11.492 | 275.301 | 10.166 | 2.741 | 0.04× | 0.04× | 0.04× | 0.04× | 0.04× | 0.01× |
| Sieve of Eratosthenes | 200000 | 1.839 | 0.996 | 1.772 | 1.020 | 17.912 | 3.058 | 0.517 | 0.10× | 0.06× | 0.10× | 0.06× | 0.17× | 0.03× |
| Quicksort | 30000 | 6.230 | 3.258 | 5.955 | 3.145 | 36.178 | 4.067 | 2.181 | 0.17× | 0.09× | 0.16× | 0.09× | 0.11× | 0.06× |
| Matrix multiplication | 150 | 7.784 | 3.192 | 8.075 | 3.194 | 293.275 | 6.128 | 2.417 | 0.03× | 0.01× | 0.03× | 0.01× | 0.02× | 0.01× |
| Mandelbrot set | 300 | 5.904 | 5.752 | 5.873 | 6.632 | 203.954 | 4.356 | 4.670 | 0.03× | 0.03× | 0.03× | 0.03× | 0.02× | 0.02× |
| N-Queens | 10 | 7.954 | 5.755 | 8.500 | 5.978 | 132.282 | 5.223 | 3.829 | 0.06× | 0.04× | 0.06× | 0.05× | 0.04× | 0.03× |
| Binary trees | 16 | 62.116 | 62.403 | 55.359 | 56.589 | 507.089 | 16.463 | 23.338 | 0.12× | 0.12× | 0.11× | 0.11× | 0.03× | 0.05× |
| Spectral norm | 250 | 6.733 | 5.336 | 6.865 | 5.079 | 374.645 | 9.691 | 2.971 | 0.02× | 0.01× | 0.02× | 0.01× | 0.03× | 0.01× |
| Collatz conjecture | 100000 | 22.737 | 23.949 | 23.353 | 24.237 | 872.467 | 61.007 | 24.811 | 0.03× | 0.03× | 0.03× | 0.03× | 0.07× | 0.03× |

### AquariusLang (typed) vs Node.js (warmed mode)

Ratio = Node.js median time ÷ AquariusLang (typed) median time; above 1 means AquariusLang (typed) is faster, below 1 means Node.js is faster.

| Benchmark | n | AquariusLang (typed) median | Node.js median | Node.js ÷ AquariusLang (typed) | Faster |
| --- | ---: | ---: | ---: | ---: | --- |
| Recursive Fibonacci | 32 | 13.602 | 18.889 | 1.39× | AquariusLang (typed), 1.39× faster |
| Ackermann function | 8 | 11.099 | 10.166 | 0.92× | Node.js, 1.09× faster |
| Sieve of Eratosthenes | 200000 | 0.996 | 3.058 | 3.07× | AquariusLang (typed), 3.07× faster |
| Quicksort | 30000 | 3.258 | 4.067 | 1.25× | AquariusLang (typed), 1.25× faster |
| Matrix multiplication | 150 | 3.192 | 6.128 | 1.92× | AquariusLang (typed), 1.92× faster |
| Mandelbrot set | 300 | 5.752 | 4.356 | 0.76× | Node.js, 1.32× faster |
| N-Queens | 10 | 5.755 | 5.223 | 0.91× | Node.js, 1.10× faster |
| Binary trees | 16 | 62.403 | 16.463 | 0.26× | Node.js, 3.79× faster |
| Spectral norm | 250 | 5.336 | 9.691 | 1.82× | AquariusLang (typed), 1.82× faster |
| Collatz conjecture | 100000 | 23.949 | 61.007 | 2.55× | AquariusLang (typed), 2.55× faster |
| **Geometric mean** | | | | **1.23×** | AquariusLang (typed), 1.23× faster |

### Timing variability (warmed mode)

Coefficient of variation (CV) = sample standard deviation of the process values ÷ their mean. With a single sample the variability cannot be estimated and a dash is shown.

| Benchmark | Language | Min ms | Max ms | Std dev ms | CV | Valid samples |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Recursive Fibonacci | AquariusLang | 13.211 | 15.366 | 0.779 | 5.5% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed) | 11.892 | 14.963 | 1.190 | 8.8% | 5/5 |
| Recursive Fibonacci | AquariusLang (Native AOT compiler) | 12.860 | 18.206 | 2.424 | 16.0% | 5/5 |
| Recursive Fibonacci | AquariusLang (typed, Native AOT compiler) | 12.578 | 17.886 | 2.150 | 13.6% | 5/5 |
| Recursive Fibonacci | Python | 212.843 | 277.865 | 24.445 | 9.6% | 5/5 |
| Recursive Fibonacci | Node.js | 18.167 | 18.979 | 0.415 | 2.2% | 5/5 |
| Recursive Fibonacci | C# | 5.880 | 8.002 | 0.800 | 11.3% | 5/5 |
| Ackermann function | AquariusLang | 9.326 | 11.797 | 0.945 | 8.9% | 5/5 |
| Ackermann function | AquariusLang (typed) | 9.834 | 11.994 | 0.921 | 8.5% | 5/5 |
| Ackermann function | AquariusLang (Native AOT compiler) | 9.683 | 11.064 | 0.647 | 6.2% | 5/5 |
| Ackermann function | AquariusLang (typed, Native AOT compiler) | 9.303 | 11.965 | 1.079 | 9.6% | 5/5 |
| Ackermann function | Python | 259.961 | 289.931 | 12.601 | 4.6% | 5/5 |
| Ackermann function | Node.js | 9.094 | 10.239 | 0.544 | 5.6% | 5/5 |
| Ackermann function | C# | 2.252 | 3.224 | 0.431 | 15.8% | 5/5 |
| Sieve of Eratosthenes | AquariusLang | 1.382 | 1.967 | 0.240 | 13.7% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed) | 0.944 | 1.068 | 0.051 | 5.1% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (Native AOT compiler) | 1.618 | 1.916 | 0.114 | 6.4% | 5/5 |
| Sieve of Eratosthenes | AquariusLang (typed, Native AOT compiler) | 0.914 | 1.069 | 0.072 | 7.2% | 5/5 |
| Sieve of Eratosthenes | Python | 13.036 | 19.070 | 2.363 | 13.8% | 5/5 |
| Sieve of Eratosthenes | Node.js | 2.928 | 3.564 | 0.244 | 7.8% | 5/5 |
| Sieve of Eratosthenes | C# | 0.515 | 0.523 | 0.003 | 0.6% | 5/5 |
| Quicksort | AquariusLang | 5.708 | 7.655 | 0.775 | 12.1% | 5/5 |
| Quicksort | AquariusLang (typed) | 2.903 | 3.387 | 0.218 | 6.9% | 5/5 |
| Quicksort | AquariusLang (Native AOT compiler) | 5.553 | 6.936 | 0.522 | 8.6% | 5/5 |
| Quicksort | AquariusLang (typed, Native AOT compiler) | 2.609 | 3.273 | 0.265 | 8.6% | 5/5 |
| Quicksort | Python | 31.095 | 37.667 | 2.844 | 8.1% | 5/5 |
| Quicksort | Node.js | 3.696 | 4.768 | 0.421 | 10.1% | 5/5 |
| Quicksort | C# | 1.997 | 2.437 | 0.159 | 7.2% | 5/5 |
| Matrix multiplication | AquariusLang | 7.428 | 10.066 | 1.130 | 13.5% | 5/5 |
| Matrix multiplication | AquariusLang (typed) | 2.554 | 3.704 | 0.490 | 15.2% | 5/5 |
| Matrix multiplication | AquariusLang (Native AOT compiler) | 7.265 | 9.222 | 0.707 | 8.7% | 5/5 |
| Matrix multiplication | AquariusLang (typed, Native AOT compiler) | 2.633 | 3.761 | 0.402 | 12.6% | 5/5 |
| Matrix multiplication | Python | 265.369 | 304.630 | 15.190 | 5.2% | 5/5 |
| Matrix multiplication | Node.js | 4.151 | 6.866 | 1.061 | 17.9% | 5/5 |
| Matrix multiplication | C# | 2.277 | 2.625 | 0.129 | 5.3% | 5/5 |
| Mandelbrot set | AquariusLang | 5.462 | 6.006 | 0.233 | 4.0% | 5/5 |
| Mandelbrot set | AquariusLang (typed) | 5.005 | 6.501 | 0.650 | 11.3% | 5/5 |
| Mandelbrot set | AquariusLang (Native AOT compiler) | 5.492 | 6.360 | 0.400 | 6.8% | 5/5 |
| Mandelbrot set | AquariusLang (typed, Native AOT compiler) | 5.595 | 7.101 | 0.686 | 10.8% | 5/5 |
| Mandelbrot set | Python | 176.205 | 230.558 | 22.766 | 11.3% | 5/5 |
| Mandelbrot set | Node.js | 3.516 | 4.821 | 0.511 | 11.9% | 5/5 |
| Mandelbrot set | C# | 4.314 | 5.030 | 0.260 | 5.6% | 5/5 |
| N-Queens | AquariusLang | 7.033 | 9.178 | 0.808 | 10.2% | 5/5 |
| N-Queens | AquariusLang (typed) | 5.367 | 6.399 | 0.421 | 7.3% | 5/5 |
| N-Queens | AquariusLang (Native AOT compiler) | 6.427 | 12.819 | 2.362 | 25.7% | 5/5 |
| N-Queens | AquariusLang (typed, Native AOT compiler) | 4.839 | 7.440 | 0.991 | 16.4% | 5/5 |
| N-Queens | Python | 118.126 | 141.517 | 8.661 | 6.6% | 5/5 |
| N-Queens | Node.js | 4.817 | 6.341 | 0.611 | 11.2% | 5/5 |
| N-Queens | C# | 2.883 | 4.530 | 0.621 | 16.2% | 5/5 |
| Binary trees | AquariusLang | 50.495 | 75.128 | 9.453 | 15.2% | 5/5 |
| Binary trees | AquariusLang (typed) | 50.885 | 66.962 | 6.248 | 10.4% | 5/5 |
| Binary trees | AquariusLang (Native AOT compiler) | 49.033 | 64.325 | 6.183 | 10.9% | 5/5 |
| Binary trees | AquariusLang (typed, Native AOT compiler) | 52.841 | 69.070 | 6.190 | 10.5% | 5/5 |
| Binary trees | Python | 502.050 | 612.601 | 47.167 | 8.9% | 5/5 |
| Binary trees | Node.js | 13.206 | 21.257 | 2.980 | 18.0% | 5/5 |
| Binary trees | C# | 17.786 | 24.636 | 2.721 | 12.3% | 5/5 |
| Spectral norm | AquariusLang | 5.537 | 7.294 | 0.670 | 10.3% | 5/5 |
| Spectral norm | AquariusLang (typed) | 5.080 | 5.784 | 0.284 | 5.3% | 5/5 |
| Spectral norm | AquariusLang (Native AOT compiler) | 6.848 | 7.029 | 0.088 | 1.3% | 5/5 |
| Spectral norm | AquariusLang (typed, Native AOT compiler) | 4.568 | 5.417 | 0.348 | 7.0% | 5/5 |
| Spectral norm | Python | 334.214 | 386.838 | 25.662 | 7.0% | 5/5 |
| Spectral norm | Node.js | 8.186 | 11.909 | 1.338 | 13.5% | 5/5 |
| Spectral norm | C# | 2.276 | 3.180 | 0.356 | 12.4% | 5/5 |
| Collatz conjecture | AquariusLang | 18.988 | 25.295 | 2.403 | 10.9% | 5/5 |
| Collatz conjecture | AquariusLang (typed) | 18.978 | 24.570 | 2.305 | 10.1% | 5/5 |
| Collatz conjecture | AquariusLang (Native AOT compiler) | 21.203 | 27.809 | 2.419 | 10.2% | 5/5 |
| Collatz conjecture | AquariusLang (typed, Native AOT compiler) | 20.596 | 24.573 | 1.652 | 7.1% | 5/5 |
| Collatz conjecture | Python | 767.009 | 931.253 | 61.870 | 7.2% | 5/5 |
| Collatz conjecture | Node.js | 49.410 | 62.407 | 5.296 | 9.1% | 5/5 |
| Collatz conjecture | C# | 20.099 | 29.561 | 3.540 | 14.5% | 5/5 |

## AquariusLang compiler build and start times

Each AquariusLang candidate builds every program with its own `aqua` (`aqua build`) and runs it (`aqua run`). Workload timings exclude both; the table shows the median build time over every benchmark and mode, and per mode the median whole-process time (starting `aqua` and the runtime included).

| Candidate | Median build | Median process, standard mode | Median process, warmed mode |
| --- | ---: | ---: | ---: |
| AquariusLang | 254.2 ms | 192.7 ms | 296.0 ms |
| AquariusLang (typed) | 238.3 ms | 197.7 ms | 255.9 ms |
| AquariusLang (Native AOT compiler) | 48.5 ms | 91.0 ms | 206.9 ms |
| AquariusLang (typed, Native AOT compiler) | 47.6 ms | 119.6 ms | 184.7 ms |

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

- Started: 2026-11-18T14:02:01.290329+08:00
- Finished: 2026-11-18T14:09:45.087448+08:00
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

- Raw samples, outputs, commands, execution order, environment and executable and source hashes: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261118-140201-290329\results.json`
- Summary and per-sample CSV: `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261118-140201-290329\summary.csv`, `C:\OfficialProjects\AquariusLang_PerformanceBenchmark\results\20261118-140201-290329\samples.csv`
- `benchmarks.json`: the standard and smoke-check input sizes and workload definitions.
- `benchmarks/aquarius/`, `benchmarks/aquarius_typed/`, `benchmarks/aquarius_aot/`, `benchmarks/aquarius_typed_aot/`, `benchmarks/python/`, `benchmarks/node/`, `benchmarks/csharp/`: the standalone benchmark programs.
- `reference.py`: the untimed reference answers; `tests/`: regression tests for the harness and reference answers.

This README and `README.tw.md` (Traditional Chinese) are generated by `run_benchmarks.py` from the same report and are overwritten on the next run. The JSON keeps the hashes of the original and staged scripts, the test list, the harness and the reference answers at measurement time. Temporary paths in the commands refer to that run's files and are removed after the run. Keep the sources and the matching report when comparing different runs.

from time import perf_counter_ns
benchmark_n = 28
benchmark_warmups = 0
benchmark_timed_runs = 1

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def benchmark_run():
    return fib(benchmark_n)

# Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for benchmark_warmup in range(benchmark_warmups):
    benchmark_run()
for benchmark_round in range(benchmark_timed_runs):
    benchmark_start = perf_counter_ns()
    benchmark_result = benchmark_run()
    benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
    print("RESULT", benchmark_result)
    print("ELAPSED_MS", benchmark_elapsed_ms)

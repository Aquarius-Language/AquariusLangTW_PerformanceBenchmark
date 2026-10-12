from time import perf_counter_ns
benchmark_n = 28

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

benchmark_start = perf_counter_ns()
benchmark_result = fib(benchmark_n)
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

from time import perf_counter_ns
import sys
sys.setrecursionlimit(10000)
benchmark_n = 6

def ack(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))

def benchmark_run():
    return ack(3, benchmark_n)

# Untimed warm-up runs, identical in every language.
for benchmark_warmup in range(3):
    benchmark_run()
benchmark_start = perf_counter_ns()
benchmark_result = benchmark_run()
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

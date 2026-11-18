from time import perf_counter_ns
benchmark_n = 1000
benchmark_warmups = 0
benchmark_timed_runs = 1

# Fills a hash with n / 5 integer keys, then reads n of them.
def benchmark_run():
    size = benchmark_n // 5
    table = {}
    for i in range(size):
        table[i * 7] = i
    total = 0
    for i in range(benchmark_n):
        total = (total + table[((i * 13) % size) * 7]) % 1000003
    return total

# Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for benchmark_warmup in range(benchmark_warmups):
    benchmark_run()
for benchmark_round in range(benchmark_timed_runs):
    benchmark_start = perf_counter_ns()
    benchmark_result = benchmark_run()
    benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
    print("RESULT", benchmark_result)
    print("ELAPSED_MS", benchmark_elapsed_ms)

from time import perf_counter_ns
benchmark_n = 10000
benchmark_warmups = 0
benchmark_timed_runs = 1
def benchmark_run():
    checksum = 0
    for start in range(1, benchmark_n + 1):
        value = start
        while value != 1:
            half = value // 2
            if half * 2 == value:
                value = half
            else:
                value = value * 3 + 1
            checksum += 1
    return checksum

# Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for benchmark_warmup in range(benchmark_warmups):
    benchmark_run()
for benchmark_round in range(benchmark_timed_runs):
    benchmark_start = perf_counter_ns()
    benchmark_result = benchmark_run()
    benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
    print("RESULT", benchmark_result)
    print("ELAPSED_MS", benchmark_elapsed_ms)

from time import perf_counter_ns
benchmark_n = 1000
benchmark_warmups = 0
benchmark_timed_runs = 1

# Appends to a string that a closure can also see.
def benchmark_run():
    text = ""
    def size():
        return len(text)
    for i in range(benchmark_n):
        text = text + "ab,"
    return size()

# Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for benchmark_warmup in range(benchmark_warmups):
    benchmark_run()
for benchmark_round in range(benchmark_timed_runs):
    benchmark_start = perf_counter_ns()
    benchmark_result = benchmark_run()
    benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
    print("RESULT", benchmark_result)
    print("ELAPSED_MS", benchmark_elapsed_ms)

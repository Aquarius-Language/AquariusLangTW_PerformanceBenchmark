from time import perf_counter_ns
benchmark_n = 1000
benchmark_warmups = 0
benchmark_timed_runs = 1

# Counts string keys in a hash: one read and one write per update, 1000 distinct keys.
def benchmark_run():
    keys = ["key" + str(j) for j in range(1000)]
    counts = {}
    for i in range(benchmark_n):
        key = keys[i % 1000]
        counts[key] = counts.get(key, 0) + 1
    return counts.get("key7", 0) * 1000 + len(counts)

# Untimed in-process warm-up runs, then timed runs; the harness substitutes both counts.
for benchmark_warmup in range(benchmark_warmups):
    benchmark_run()
for benchmark_round in range(benchmark_timed_runs):
    benchmark_start = perf_counter_ns()
    benchmark_result = benchmark_run()
    benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
    print("RESULT", benchmark_result)
    print("ELAPSED_MS", benchmark_elapsed_ms)

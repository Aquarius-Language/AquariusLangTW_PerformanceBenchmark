from time import perf_counter_ns
benchmark_n = 1000
benchmark_warmups = 0
benchmark_timed_runs = 1

# Maps an array with a function literal, then calls a closure that updates a captured variable n times.
def benchmark_run():
    doubled = list(map(lambda x: x * 2, [1] * benchmark_n))
    total = 0
    def add(value):
        nonlocal total
        total = (total + value) % 1000003
    for i in range(benchmark_n):
        add(doubled[i] + i % 3)
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

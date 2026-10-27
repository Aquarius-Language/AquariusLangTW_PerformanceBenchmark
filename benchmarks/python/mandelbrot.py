from time import perf_counter_ns
benchmark_n = 80
benchmark_warmups = 0
benchmark_timed_runs = 1
def benchmark_run():
    checksum = 0
    for y in range(benchmark_n):
        ci = 2.0 * y / benchmark_n - 1.0
        for x in range(benchmark_n):
            cr = 3.0 * x / benchmark_n - 2.0
            zr, zi, count = 0.0, 0.0, 0
            while count < 60 and zr * zr + zi * zi <= 4.0:
                next_r = zr * zr - zi * zi + cr
                zi = 2.0 * zr * zi + ci
                zr = next_r
                count += 1
            checksum += count
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

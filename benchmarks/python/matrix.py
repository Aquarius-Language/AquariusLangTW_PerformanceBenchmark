from time import perf_counter_ns
benchmark_n = 45
benchmark_start = perf_counter_ns()
a, b = [], []
for i in range(benchmark_n):
    for j in range(benchmark_n):
        x, y = i + j, i * 2 + j
        a = a + [x - (x // 7) * 7]
        b = b + [y - (y // 5) * 5]
checksum = 0
for i in range(benchmark_n):
    for j in range(benchmark_n):
        total = 0
        for k in range(benchmark_n):
            total += a[i * benchmark_n + k] * b[k * benchmark_n + j]
        checksum += total
benchmark_result = checksum
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

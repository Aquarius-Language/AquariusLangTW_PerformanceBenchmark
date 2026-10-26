from time import perf_counter_ns
benchmark_n = 2000
def sort(a, lo, hi):
    i, j = lo, hi
    pivot = a[(lo + hi) // 2]
    while i <= j:
        while a[i] < pivot:
            i += 1
        while a[j] > pivot:
            j -= 1
        if i <= j:
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp
            i += 1
            j -= 1
    if lo < j:
        sort(a, lo, j)
    if i < hi:
        sort(a, i, hi)

benchmark_start = perf_counter_ns()
values = []
seed = 42
for i in range(benchmark_n):
    raw = seed * 251 + 17
    seed = raw - (raw // 65536) * 65536
    values.append(seed)

sort(values, 0, benchmark_n - 1)
checksum = 0
for i in range(benchmark_n):
    if i > 0 and values[i] < values[i - 1]:
        raise RuntimeError("Unsorted output")
    checksum += values[i] * (i + 1)
    checksum -= (checksum // 1000003) * 1000003
benchmark_result = checksum
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

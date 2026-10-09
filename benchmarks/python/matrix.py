benchmark_n = 45
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
print("RESULT", checksum)

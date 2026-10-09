benchmark_n = 80
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
print("RESULT", checksum)

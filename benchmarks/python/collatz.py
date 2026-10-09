benchmark_n = 10000
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
print("RESULT", checksum)

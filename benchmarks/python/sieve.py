benchmark_n = 10000
flags = []
# Copy-and-append matches Aquarius push's allocation semantics.
for i in range(benchmark_n + 1):
    flags = flags + [True]
flags[0] = False
flags[1] = False
p = 2
while p * p <= benchmark_n:
    if flags[p]:
        j = p * p
        while j <= benchmark_n:
            flags[j] = False
            j += p
    p += 1
count = 0
for i in range(2, benchmark_n + 1):
    if flags[i]:
        count += 1
print("RESULT", count)

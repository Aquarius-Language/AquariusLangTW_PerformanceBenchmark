from time import perf_counter_ns
benchmark_n = 60

def element(i, j):
    s = i + j
    return 1.0 / (s * (s + 1) // 2 + i + 1)

def multiply(src, dst, transpose):
    for i in range(benchmark_n):
        total = 0.0
        for j in range(benchmark_n):
            coefficient = element(j, i) if transpose else element(i, j)
            total += coefficient * src[j]
        dst[i] = total

benchmark_start = perf_counter_ns()
u, v, temp = [], [], []
for i in range(benchmark_n):
    u = u + [1.0]
    v = v + [0.0]
    temp = temp + [0.0]
for iteration in range(10):
    multiply(u, temp, False)
    multiply(temp, v, True)
    multiply(v, temp, False)
    multiply(temp, u, True)
uv, vv = 0.0, 0.0
for i in range(benchmark_n):
    uv += u[i] * v[i]
    vv += v[i] * v[i]
benchmark_result = uv / vv
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

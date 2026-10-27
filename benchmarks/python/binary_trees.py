from time import perf_counter_ns
benchmark_n = 12

def build(depth):
    if depth == 0:
        return [0, 0]
    return [build(depth - 1), build(depth - 1)]

def check(tree, depth):
    if depth == 0:
        return 1
    return 1 + check(tree[0], depth - 1) + check(tree[1], depth - 1)

def benchmark_run():
    checksum = 0
    for i in range(8):
        tree = build(benchmark_n)
        checksum += check(tree, benchmark_n)
    return checksum

# Untimed warm-up runs, identical in every language.
for benchmark_warmup in range(3):
    benchmark_run()
benchmark_start = perf_counter_ns()
benchmark_result = benchmark_run()
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

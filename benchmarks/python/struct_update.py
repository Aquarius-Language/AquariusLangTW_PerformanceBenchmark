from time import perf_counter_ns
benchmark_n = 1000
benchmark_warmups = 0
benchmark_timed_runs = 1

# Updates 1000 struct particles through a step function, n calls in all.
class Particle:
    __slots__ = ("x", "v")
    def __init__(self, x, v):
        self.x = x
        self.v = v

def step(p):
    p.x = (p.x + p.v) % 10007
    return p.x

def benchmark_run():
    particles = [Particle(j, j % 17 + 1) for j in range(1000)]
    total = 0
    for i in range(benchmark_n):
        total = (total + step(particles[i % 1000])) % 1000003
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

benchmark_n = 28

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print("RESULT", fib(benchmark_n))

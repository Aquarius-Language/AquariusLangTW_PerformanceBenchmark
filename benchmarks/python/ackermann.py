import sys
sys.setrecursionlimit(10000)
benchmark_n = 6

def ack(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))

print("RESULT", ack(3, benchmark_n))

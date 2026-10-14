"""Untimed correctness oracles, intentionally using alternative approaches where possible."""
import math


def expected(name, n):
    if name == "fibonacci":
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    if name == "ackermann":
        return 2 ** (n + 3) - 3
    if name == "sieve":
        return sum(all(p % d for d in range(2, math.isqrt(p) + 1)) for p in range(2, n + 1))
    if name == "quicksort":
        seed, values = 42, []
        for _ in range(n):
            seed = (seed * 251 + 17) % 65536
            values.append(seed)
        return sum((i + 1) * x for i, x in enumerate(sorted(values))) % 1000003
    if name == "matrix":
        # Sum(C) = sum_k(column_sum(A, k) * row_sum(B, k)).
        return sum(sum((i + k) % 7 for i in range(n)) *
                   sum((2 * k + j) % 5 for j in range(n)) for k in range(n))
    if name == "mandelbrot":
        checksum = 0
        for y in range(n):
            for x in range(n):
                c = complex(3.0 * x / n - 2.0, 2.0 * y / n - 1.0)
                z, count = 0j, 0
                while count < 60 and z.real * z.real + z.imag * z.imag <= 4.0:
                    z = z * z + c
                    count += 1
                checksum += count
        return checksum
    if name == "nqueens":
        def solve(row, cols, diagonal_a, diagonal_b):
            if row == n:
                return 1
            return sum(solve(row + 1, cols | {col}, diagonal_a | {row - col},
                             diagonal_b | {row + col})
                       for col in range(n) if col not in cols and row - col not in diagonal_a
                       and row + col not in diagonal_b)
        return solve(0, set(), set(), set())
    if name == "binary_trees":
        return 8 * (2 ** (n + 1) - 1)
    if name == "spectral_norm":
        matrix = [[1.0 / ((i + j) * (i + j + 1) // 2 + i + 1)
                   for j in range(n)] for i in range(n)]
        transpose = list(zip(*matrix))
        def multiply(a, v):
            return [sum(x * y for x, y in zip(row, v)) for row in a]
        def ata(v):
            return multiply(transpose, multiply(matrix, v))
        u = [1.0] * n
        for _ in range(10):
            v = ata(u)
            u = ata(v)
        return sum(x * y for x, y in zip(u, v)) / sum(y * y for y in v)
    if name == "collatz":
        lengths = {1: 0}
        checksum = 0
        for start in range(1, n + 1):
            path, value = [], start
            while value not in lengths:
                path.append(value)
                value = value // 2 if value % 2 == 0 else 3 * value + 1
            steps = lengths[value]
            for value in reversed(path):
                steps += 1
                lengths[value] = steps
            checksum += lengths[start]
        return checksum
    raise ValueError(f"Unknown benchmark: {name}")

from time import perf_counter_ns
benchmark_n = 8
def solve(row):
    if row == benchmark_n:
        return 1
    count = 0
    for col in range(benchmark_n):
        safe = True
        for prev in range(row):
            delta = row - prev
            if board[prev] == col or board[prev] == col - delta or board[prev] == col + delta:
                safe = False
                break
        if safe:
            board[row] = col
            count += solve(row + 1)
    return count

benchmark_start = perf_counter_ns()
board = []
for i in range(benchmark_n):
    board = board + [0]

benchmark_result = solve(0)
benchmark_elapsed_ms = (perf_counter_ns() - benchmark_start) / 1e6
print("RESULT", benchmark_result)
print("ELAPSED_MS", benchmark_elapsed_ms)

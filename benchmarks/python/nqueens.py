benchmark_n = 8
board = []
for i in range(benchmark_n):
    board = board + [0]

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

print("RESULT", solve(0))

benchmark_n = 12

def build(depth):
    if depth == 0:
        return [0, 0]
    return [build(depth - 1), build(depth - 1)]

def check(tree, depth):
    if depth == 0:
        return 1
    return 1 + check(tree[0], depth - 1) + check(tree[1], depth - 1)

checksum = 0
for i in range(8):
    tree = build(benchmark_n)
    checksum += check(tree, benchmark_n)
print("RESULT", checksum)

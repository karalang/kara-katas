# Benchmark for #404: mirror of sum_of_left_leaves.kara (recursion that
# knows which side it came from), over the same index pool.
import sys

sys.setrecursionlimit(30000)


def visit(nodes, node, is_left):
    if node == -1:
        return 0
    val, left, right = nodes[node]
    if left == -1 and right == -1:
        return val if is_left else 0
    return visit(nodes, left, True) + visit(nodes, right, False)


def sum_of_left_leaves(nodes):
    if not nodes:
        return 0
    return visit(nodes, 0, False)


def main():
    trees = 50
    n = 30000
    rounds = 50
    seed = 404
    total = 0
    checksum = 0

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    for _ in range(trees):
        nodes = [[step() % 201 - 100, -1, -1]]
        for i in range(1, n):
            p = step() % i
            side = 1 + step() % 2
            while nodes[p][side] != -1:
                p = step() % i
                side = 1 + step() % 2
            nodes.append([step() % 201 - 100, -1, -1])
            nodes[p][side] = i
        for r in range(rounds):
            nodes[r][0] += 1
            s = sum_of_left_leaves(nodes)
            total += s
            checksum = (checksum * 31 + s + 10000000 + r) % 1000000007
    print(f"{trees} trees of {n} nodes, {rounds} rounds: total {total}, checksum {checksum}")


main()

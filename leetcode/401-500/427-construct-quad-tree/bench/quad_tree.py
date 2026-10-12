# Benchmark for #427: mirror of quad_tree.kara (divide, then merge).
# A leaf is ("leaf", value), a split is ("split", tl, tr, bl, br).
import sys


def build(grid, row, col, size):
    if size == 1:
        return ("leaf", grid[row][col] == 1)
    half = size // 2
    top_left = build(grid, row, col, half)
    top_right = build(grid, row, col + half, half)
    bottom_left = build(grid, row + half, col, half)
    bottom_right = build(grid, row + half, col + half, half)
    if top_left[0] == "leaf" and top_right[0] == "leaf" and bottom_left[0] == "leaf" and bottom_right[0] == "leaf":
        if top_left[1] == top_right[1] == bottom_left[1] == bottom_right[1]:
            return ("leaf", top_left[1])
    return ("split", top_left, top_right, bottom_left, bottom_right)


def construct(grid):
    return build(grid, 0, 0, len(grid))


seed = 427


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count(q):
    if q[0] == "leaf":
        return 1
    return 1 + count(q[1]) + count(q[2]) + count(q[3]) + count(q[4])


def main():
    n = 64
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    grid = [[0] * n for _ in range(n)]
    total = 0
    checksum = 0
    for _ in range(rounds):
        size = 1 << (step() % 7)
        top = step() % (n // size) * size
        left = step() % (n // size) * size
        v = step() % 2
        for r in range(top, top + size):
            row = grid[r]
            for c in range(left, left + size):
                row[c] = v
        r = step() % n
        c = step() % n
        grid[r][c] = 1 - grid[r][c]
        nodes = count(construct(grid))
        total += nodes
        checksum = (checksum * 31 + nodes) % 1000000007
    print(f"{rounds} rounds on a {n} by {n} grid: {total} nodes, checksum {checksum}")


main()

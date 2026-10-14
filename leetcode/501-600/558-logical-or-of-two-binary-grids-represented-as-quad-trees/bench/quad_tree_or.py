# Benchmark for #558: Python mirror of the ★ arm (recursion, then a
# merge); see quad_tree_or.kara. A leaf is (True, value) and a split is
# (False, top_left, top_right, bottom_left, bottom_right); the answer
# shares the subtrees it keeps with the two trees.


def merge(k0, k1, k2, k3):
    if k0[0] and k1[0] and k2[0] and k3[0] and k0[1] == k1[1] == k2[1] == k3[1]:
        return (True, k0[1])
    return (False, k0, k1, k2, k3)


def intersect(a, b):
    if a[0]:
        return a if a[1] else b
    if b[0]:
        return b if b[1] else a
    return merge(intersect(a[1], b[1]), intersect(a[2], b[2]),
                 intersect(a[3], b[3]), intersect(a[4], b[4]))


# ---- benchmark ---------------------------------------------------------------


def build(grid, row, col, size):
    if size == 1:
        return (True, grid[row][col] == 1)
    half = size // 2
    return merge(build(grid, row, col, half), build(grid, row, col + half, half),
                 build(grid, row + half, col, half), build(grid, row + half, col + half, half))


def count(q):
    if q[0]:
        return 1
    return 1 + count(q[1]) + count(q[2]) + count(q[3]) + count(q[4])


def main():
    n = 64
    count_trees = 200
    rounds = 300
    seed = 558

    def step():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    trees = []
    for _ in range(count_trees):
        block = 1 << (step() % 5)
        grid = [[0] * n for _ in range(n)]
        for br in range(n // block):
            for bc in range(n // block):
                v = 1 if step() % 3 == 0 else 0
                for r in range(block):
                    for c in range(block):
                        grid[br * block + r][bc * block + c] = v
        for _ in range(40):
            r = step() % n
            c = step() % n
            grid[r][c] = 1 - grid[r][c]
        trees.append(build(grid, 0, 0, n))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for i in range(count_trees):
            other = (i * 7 + rnd + 1) % count_trees
            nodes = count(intersect(trees[i], trees[other]))
            total += nodes
            checksum = (checksum * 31 + nodes) % 1000000007
    print(f"{count_trees} trees, {rounds} rounds: {total} nodes, checksum {checksum}")


main()

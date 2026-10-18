# LeetCode #695: Max Area of Island -- bench program, Python mirror of the union-find arm.

seed = 695


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def join(parent, size, a, b):
    x, y = find(parent, a), find(parent, b)
    if x == y:
        return
    if size[x] < size[y]:
        x, y = y, x
    parent[y] = x
    size[x] += size[y]


def max_area_of_island(grid):
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))
    size = [1] * (m * n)
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                continue
            if r + 1 < m and grid[r + 1][c] == 1:
                join(parent, size, r * n + c, (r + 1) * n + c)
            if c + 1 < n and grid[r][c + 1] == 1:
                join(parent, size, r * n + c, r * n + c + 1)
    best = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and find(parent, r * n + c) == r * n + c:
                best = max(best, size[r * n + c])
    return best


def main():
    grids = []
    for _ in range(40):
        percent = 30 + next_random() % 41
        grids.append([[1 if next_random() % 100 < percent else 0 for _ in range(50)] for _ in range(50)])
    rounds = 300
    total = 0
    checksum = 0
    for _ in range(rounds):
        for grid in grids:
            r = max_area_of_island(grid)
            total += r
            checksum = (checksum * 31 + r) % 1000000007
    print(f"{rounds} rounds of 40 grids of 50 by 50: largest areas sum to {total}, checksum {checksum}")


main()

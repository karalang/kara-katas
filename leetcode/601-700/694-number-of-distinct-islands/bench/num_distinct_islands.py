# LeetCode #694: Number of Distinct Islands -- bench program, Python mirror of the union-find arm.

seed = 694


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


def num_distinct_islands(grid):
    m, n = len(grid), len(grid[0])
    parent = list(range(m * n))
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                continue
            if r + 1 < m and grid[r + 1][c] == 1:
                a = find(parent, r * n + c)
                b = find(parent, (r + 1) * n + c)
                parent[a] = b
            if c + 1 < n and grid[r][c + 1] == 1:
                a = find(parent, r * n + c)
                b = find(parent, r * n + c + 1)
                parent[a] = b
    first = [-1] * (m * n)
    slot = [-1] * (m * n)
    shapes = []
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 0:
                continue
            root = find(parent, r * n + c)
            if first[root] < 0:
                first[root] = r * n + c
                slot[root] = len(shapes)
                shapes.append([])
            r0, c0 = first[root] // n, first[root] % n
            shapes[slot[root]].append((r - r0) * 200 + (c - c0))
    shapes.sort()
    distinct = 0
    for i in range(len(shapes)):
        if i == 0 or shapes[i] != shapes[i - 1]:
            distinct += 1
    return distinct


def main():
    grids = []
    for _ in range(40):
        percent = 30 + next_random() % 31
        grids.append([[1 if next_random() % 100 < percent else 0 for _ in range(50)] for _ in range(50)])
    rounds = 150
    total = 0
    checksum = 0
    for _ in range(rounds):
        for grid in grids:
            r = num_distinct_islands(grid)
            total += r
            checksum = (checksum * 31 + r) % 1000000007
    print(f"{rounds} rounds of 40 grids of 50 by 50: {total} distinct islands counted, checksum {checksum}")


main()

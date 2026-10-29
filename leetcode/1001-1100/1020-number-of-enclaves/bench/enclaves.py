# LeetCode #1020: Number of Enclaves -- bench
# Mirrors ./enclaves.kara; see ../README.md § Benchmarks.


def num_enclaves(grid):
    m = len(grid)
    n = len(grid[0])
    land = [row[:] for row in grid]
    stack = []
    for i in range(m):
        for j in range(n):
            if (i == 0 or j == 0 or i == m - 1 or j == n - 1) and land[i][j] == 1:
                land[i][j] = 0
                stack.append((i, j))
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while stack:
        i, j = stack.pop()
        for di, dj in steps:
            a, b = i + di, j + dj
            if 0 <= a < m and 0 <= b < n and land[a][b] == 1:
                land[a][b] = 0
                stack.append((a, b))
    left = 0
    for row in land:
        for c in row:
            left += c
    return left


def main():
    count = 100
    rounds = 20
    seed = 1020

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = []
    cells = 0
    for _ in range(count):
        m = next_random() % 500 + 1
        n = next_random() % 500 + 1
        land = 2 + next_random() % 5
        grid = []
        for _ in range(m):
            row = []
            for _ in range(n):
                row.append(1 if next_random() % 8 < land else 0)
            grid.append(row)
        cells += m * n
        grids.append(grid)
    total = 0
    check = 0
    for _ in range(rounds):
        for grid in grids:
            a = num_enclaves(grid)
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"{count} grids, {cells} cells, {rounds} rounds: {total} enclaves, checksum {check}")


main()

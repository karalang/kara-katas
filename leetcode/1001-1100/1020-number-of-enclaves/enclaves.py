# LeetCode #1020: Number of Enclaves -- sinking the coast
# Mirrors enclaves.kara; its output is byte-identical.


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
    return sum(sum(row) for row in land)


seed = 1020


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, land):
    return [[1 if next_random() % 8 < land else 0 for _ in range(n)] for _ in range(m)]


def shown(grid):
    return "[" + ", ".join("[" + ", ".join(str(c) for c in row) + "]" for row in grid) + "]"


def main():
    examples = [
        [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
        [[1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
    ]
    for grid in examples:
        print(f"{shown(grid)} -> {num_enclaves(grid)}")
    groups = [(2000, 4, 4, 4), (500, 8, 12, 4), (100, 30, 30, 4), (100, 30, 30, 5), (30, 60, 80, 6), (30, 60, 80, 3)]
    for count, m, n, land in groups:
        total = most = check = 0
        for _ in range(count):
            answer = num_enclaves(random_grid(m, n, land))
            total += answer
            most = max(most, answer)
            check = (check * 31 + answer) % 1000000007
        print(f"{count} random {m}x{n} grids ({land}/8 land): {total} enclaves, most {most}, checksum {check}")
    size = 61
    spiral = []
    for i in range(size):
        row = []
        for j in range(size):
            depth = min(i, j, size - 1 - i, size - 1 - j)
            land = depth % 2 == 1 or (j == depth + 1 and i == depth and depth % 2 == 0 and depth > 0)
            row.append(1 if land and depth > 0 else 0)
        spiral.append(row)
    cells = sum(sum(row) for row in spiral)
    print(f"61x61 rings: {cells} land, {num_enclaves(spiral)} enclaves")


main()

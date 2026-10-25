# Benchmark: LeetCode #994 Rotting Oranges -- the ★ arm, a
# breadth-first search from every rotten orange at once, on random grids
# of 10 by 10, LeetCode's largest. Mirrors oranges_rotting.kara, .rs, .c
# and go-seq/.
from collections import deque


def oranges_rotting(grid):
    m = len(grid)
    n = len(grid[0])
    g = [row[:] for row in grid]
    queue = deque()
    fresh = 0
    for r in range(m):
        for c in range(n):
            if g[r][c] == 2:
                queue.append((r, c, 0))
            elif g[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = t
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < m and 0 <= nc < n and g[nr][nc] == 1:
                g[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, t + 1))
    return -1 if fresh > 0 else minutes


seed = 994


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid():
    grid = []
    for _ in range(10):
        row = []
        for _ in range(10):
            k = next_random() % 32
            row.append(0 if k < 3 else (2 if k == 3 else 1))
        grid.append(row)
    return grid


def main():
    rounds = 20000
    grids = [random_grid() for _ in range(20)]
    stuck = 0
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            got = oranges_rotting(grids[(r + i) % 20])
            if got < 0:
                stuck += 1
            else:
                total += got
            check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds over 20 grids of 10 by 10: {stuck} never rot, {total} minutes, checksum {check}")


main()

# LeetCode #1293 bench: the ★ arm over 50 grids of 40 by 40 with obstacles 30
# in 100, built once; then 80 passes, each flipping one cell of every grid and
# choosing k from the checksum so far, answering it.
from collections import deque


def shortest_path(grid, k):
    m, n = len(grid), len(grid[0])
    if k >= m + n - 2:
        return m + n - 2
    best = [[-1] * n for _ in range(m)]
    queue = deque([(0, 0, k)])
    best[0][0] = k
    steps = 0
    while queue:
        for _ in range(len(queue)):
            r, c, left = queue.popleft()
            if r == m - 1 and c == n - 1:
                return steps
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= m or nc < 0 or nc >= n:
                    continue
                rest = left - grid[nr][nc]
                if rest > best[nr][nc]:
                    best[nr][nc] = rest
                    queue.append((nr, nc, rest))
        steps += 1
    return -1


def main():
    seed = 1293

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    grids = []
    for _ in range(50):
        grid = []
        for i in range(40):
            row = []
            for j in range(40):
                corner = (i == 0 and j == 0) or (i == 39 and j == 39)
                row.append(1 if not corner and next_random() % 100 < 30 else 0)
            grid.append(row)
        grids.append(grid)
    check = 0
    for p in range(80):
        for a in range(len(grids)):
            cell = 1 + check % 1598
            grids[a][cell // 40][cell % 40] = 1 - grids[a][cell // 40][cell % 40]
            check = (check * 31 + shortest_path(grids[a], check % 78) + 2 + p) % 1000000007
    print(f"80 passes over 50 grids of 40 by 40: checksum {check}")


main()

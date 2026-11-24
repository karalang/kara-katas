# LeetCode #1293: Shortest Path in a Grid with Obstacles Elimination -- Python
# mirror of the ★ arm: a breadth-first search over (row, column, eliminations
# left), each cell keeping the most eliminations it has been reached with.
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

    def problem(m, n, percent):
        grid = []
        for i in range(m):
            row = []
            for j in range(n):
                corner = (i == 0 and j == 0) or (i == m - 1 and j == n - 1)
                row.append(1 if not corner and next_random() % 100 < percent else 0)
            grid.append(row)
        return grid

    ex1 = [[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]]
    ex2 = [[0, 1, 1], [1, 1, 1], [1, 0, 0]]
    wall = [[0, 1, 1, 1, 0]]
    print(f"{shortest_path(ex1, 1)} {shortest_path(ex2, 1)} {shortest_path([[0]], 0)} {shortest_path(wall, 3)} {shortest_path(wall, 2)}")
    total = 0
    unreachable = 0
    check = 0
    for case in range(402):
        big = case >= 400
        m = 40 if big else next_random() % 15 + 1
        n = 40 if big else next_random() % 15 + 1
        percent = 45 if big else 10 + next_random() % 61
        grid = problem(m, n, percent)
        k = 3 + case % 2 if big else next_random() % 7
        steps = shortest_path(grid, k)
        if steps < 0:
            unreachable += 1
        else:
            total += steps
        check = (check * 131 + steps + 2) % 1000000007
    print(f"402 random grids: {unreachable} unreachable, steps total {total}, checksum {check}")


main()

# LeetCode #1391 bench, Python mirror of the ★ arm.
from collections import deque

WAYS = [[], [(0, -1), (0, 1)], [(-1, 0), (1, 0)], [(0, -1), (1, 0)],
        [(0, 1), (1, 0)], [(0, -1), (-1, 0)], [(0, 1), (-1, 0)]]


def has_valid_path(grid):
    m, n = len(grid), len(grid[0])
    seen = [False] * (m * n)
    queue = deque([(0, 0)])
    seen[0] = True
    while queue:
        r, c = queue.popleft()
        if r == m - 1 and c == n - 1:
            return True
        for dr, dc in WAYS[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= m or nc < 0 or nc >= n or seen[nr * n + nc]:
                continue
            if (-dr, -dc) in WAYS[grid[nr][nc]]:
                seen[nr * n + nc] = True
                queue.append((nr, nc))
    return False


seed = 1391


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    m, n = 299, 300
    grid = [[1] * n for _ in range(m)]
    for r in range(m - 1):
        if r % 2 == 0:
            grid[r][n - 1] = 3
            grid[r + 1][n - 1] = 5
        else:
            grid[r][0] = 4
            grid[r + 1][0] = 6
    check = 0
    whole = has_valid_path(grid)
    for _ in range(3000):
        seed = (seed + check) % 2147483648
        cell = next_random() % (m * n)
        r, c = cell // n, cell % n
        street = grid[r][c]
        grid[r][c] = street % 6 + 1
        got = has_valid_path(grid)
        grid[r][c] = street
        check = (check * 131 + (2 if got else 1) * (cell + 1)) % 1000000007
    print(f"3000 rounds over a 299 by 300 snake, whole {'true' if whole else 'false'}: checksum {check}")


main()

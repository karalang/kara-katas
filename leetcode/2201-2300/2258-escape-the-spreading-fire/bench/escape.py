# LeetCode #2258: Escape the Spreading Fire -- Python mirror of the ★ arm
# (escape.kara) on the bench workload: fire times by one breadth-first
# search from every fire, then a binary search over the wait, each wait
# tried by a breadth-first search of the person. Output is byte-identical
# to escape.kara.
from collections import deque

NEVER = 1000000000000
STEPS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def fire_times(grid):
    m, n = len(grid), len(grid[0])
    at = [[NEVER] * n for _ in range(m)]
    queue = deque()
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                at[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in STEPS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and at[nr][nc] == NEVER:
                at[nr][nc] = at[r][c] + 1
                queue.append((nr, nc))
    return at


def escapes(grid, fire, wait):
    m, n = len(grid), len(grid[0])
    if wait >= fire[0][0]:
        return False
    seen = [[False] * n for _ in range(m)]
    seen[0][0] = True
    queue = deque([(0, 0, wait)])
    while queue:
        r, c, t = queue.popleft()
        for dr, dc in STEPS:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= m or nc < 0 or nc >= n or grid[nr][nc] != 0 or seen[nr][nc]:
                continue
            if nr == m - 1 and nc == n - 1:
                if t + 1 <= fire[nr][nc]:
                    return True
                continue
            if t + 1 < fire[nr][nc]:
                seen[nr][nc] = True
                queue.append((nr, nc, t + 1))
    return False


def maximum_minutes(grid):
    fire = fire_times(grid)
    cells = len(grid) * len(grid[0])
    if not escapes(grid, fire, 0):
        return -1
    if escapes(grid, fire, cells):
        return 1000000000
    lo, hi = 0, cells
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if escapes(grid, fire, mid):
            lo = mid
        else:
            hi = mid
    return lo


# ---- bench harness ---------------------------------------------------------

seed = 2258


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def chase(m, n, walls):
    grid = []
    for r in range(m):
        row = []
        for c in range(n):
            roll = next_random() % 100
            row.append(2 if c == 1 and r > 0 else 2 if c >= 2 and roll < walls else 0)
        grid.append(row)
    grid[0][2] = 0
    grid[m - 1][n - 1] = 0
    grid[next_random() % (m - 1) + 1][0] = 1
    return grid


def main():
    check = 0
    waits = 0
    shapes = [(100, 200), (200, 100), (125, 160)]
    for t in range(300):
        m, n = shapes[t % 3]
        answer = maximum_minutes(chase(m, n, 8))
        if 0 <= answer < 1000000000:
            waits += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"300 grids of 2 * 10^4 cells: {waits} with a wait, checksum {check}")


main()

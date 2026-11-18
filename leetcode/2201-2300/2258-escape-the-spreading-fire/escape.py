# LeetCode #2258: Escape the Spreading Fire -- Python mirror of the ★ arm
# (escape.kara): fire times by one breadth-first search from every fire,
# then a binary search over the wait, each wait tried by a breadth-first
# search of the person. Output is byte-identical to the Kara arms.
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid_of(m, n, walls):
    grid = []
    for _ in range(m):
        grid.append([2 if next_random() % 100 < walls else 0 for _ in range(n)])
    grid[0][0] = 0
    grid[m - 1][n - 1] = 0
    k = next_random() % (m * n - 2) + 1
    grid[k // n][k % n] = 1
    return grid


def open_grid(m, n):
    return [[0] * n for _ in range(m)]


def main():
    global seed
    examples = [
        [[0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 1, 0], [0, 2, 0, 0, 1, 2, 0], [0, 0, 2, 2, 2, 0, 2], [0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 1, 2, 0], [0, 2, 0, 0]],
        [[0, 0, 0], [2, 2, 0], [1, 2, 0]],
        [[0, 1], [0, 0]],
        [[0, 0, 0, 0], [0, 2, 0, 0], [0, 1, 2, 0]],
        [[0, 0, 0, 0, 0], [2, 2, 2, 2, 0], [1, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0], [1, 2, 2, 2, 2, 0]],
    ]
    for grid in examples:
        print(f"{grid} -> {maximum_minutes(grid)}")
    seed = 2258
    counts = [0, 0, 0]
    check = 0
    for _ in range(5000):
        m = next_random() % 10 + 2
        n = next_random() % 10 + 2
        answer = maximum_minutes(grid_of(m, n, 25))
        if answer == -1:
            counts[0] += 1
        elif answer == 1000000000:
            counts[2] += 1
        else:
            counts[1] += 1
        check = (check * 31 + answer + 1) % 1000000007
    print(f"5000 grids: {counts[0]} trapped, {counts[1]} with a wait, {counts[2]} never reached, checksum {check}")
    answers = []
    chase = open_grid(100, 200)
    for r in range(1, 100):
        chase[r][1] = 2
    chase[99][0] = 1
    answers.append(maximum_minutes(chase))
    strip = open_grid(2, 10000)
    strip[1][0] = 1
    strip[1][1] = 2
    answers.append(maximum_minutes(strip))
    winding = open_grid(300, 66)
    r = 1
    while r < 299:
        for c in range(66):
            winding[r][c] = 2
        winding[r][63 if (r // 2) % 2 == 0 else 0] = 0
        r += 2
    winding[0][65] = 1
    winding[0][64] = 2
    answers.append(maximum_minutes(winding))
    print(f"2 * 10^4 cells: {answers}")


main()

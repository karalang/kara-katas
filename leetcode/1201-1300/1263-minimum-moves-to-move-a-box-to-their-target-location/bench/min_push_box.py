# LeetCode #1263 bench, in Python: the ★ arm's 0-1 BFS over (box, player)
# states (a step to the front of a deque, a push to the back, a state final
# the first time it leaves) on 100 random 20 by 20 grids, a cell in 10 a
# wall, built once, 20 rounds; every answer folded into a checksum.
from collections import deque


def min_push_box(grid):
    m, n = len(grid), len(grid[0])
    player = box_at = target = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 'S':
                player = r * n + c
            elif grid[r][c] == 'B':
                box_at = r * n + c
            elif grid[r][c] == 'T':
                target = r * n + c
    cells = m * n
    done = [False] * (cells * cells)
    dq = deque([(box_at, player, 0)])
    while dq:
        b, p, pushes = dq.popleft()
        if done[b * cells + p]:
            continue
        done[b * cells + p] = True
        if b == target:
            return pushes
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = p // n + dr, p % n + dc
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == '#':
                continue
            q = r * n + c
            if q != b:
                dq.appendleft((b, q, pushes))
                continue
            br, bc = r + dr, c + dc
            if 0 <= br < m and 0 <= bc < n and grid[br][bc] != '#':
                dq.append((br * n + bc, q, pushes + 1))
    return -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_grid(m, n, walls, rng):
    grid = [['#' if rng.next() % walls == 0 else '.' for _ in range(n)] for _ in range(m)]
    for mark in 'SBT':
        p = rng.next() % (m * n)
        while grid[p // n][p % n] in 'SBT':
            p = (p + 1) % (m * n)
        grid[p // n][p % n] = mark
    return grid


def main():
    rng = Rng(1263)
    grids = [random_grid(20, 20, 10, rng) for _ in range(100)]
    check = total = 0
    for rnd in range(20):
        for g in grids:
            pushes = min_push_box(g)
            if pushes > 0:
                total += pushes
            check = (check * 131 + pushes + 1 + rnd) % 1000000007
    print(f"20 rounds of 100 grids of 20 by 20: {total} pushes, checksum {check}")


main()

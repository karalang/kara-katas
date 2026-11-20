# LeetCode #1263: Minimum Moves to Move a Box to Their Target Location --
# Python mirror of the ★ arm (a 0-1 BFS over (box, player) states: a step
# to the front of a deque, a push to the back, a state final the first
# time it leaves), with the same harness.
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
    one = [list(r) for r in ["######", "#T####", "#..B.#", "#.##.#", "#...S#", "######"]]
    two = [list(r) for r in ["######", "#T####", "#..B.#", "####.#", "#...S#", "######"]]
    three = [list(r) for r in ["######", "#T..##", "#.#B.#", "#....#", "#...S#", "######"]]
    print(f"{min_push_box(one)} {min_push_box(two)} {min_push_box(three)}")
    rng = Rng(1263)
    total = stuck = check = 0
    for _ in range(1000):
        m = rng.next() % 8 + 3
        n = rng.next() % 8 + 3
        pushes = min_push_box(random_grid(m, n, 8, rng))
        if pushes < 0:
            stuck += 1
        else:
            total += pushes
        check = (check * 131 + pushes + 1) % 1000000007
    print(f"1000 random grids: {total} pushes, {stuck} stuck, checksum {check}")
    open_ = [['.'] * 20 for _ in range(20)]
    open_[0][0] = 'S'
    open_[1][1] = 'B'
    open_[18][18] = 'T'
    a = min_push_box(open_)
    b = min_push_box(random_grid(20, 20, 10, rng))
    c = min_push_box(random_grid(20, 20, 10, rng))
    print(f"{a} {b} {c}")


main()

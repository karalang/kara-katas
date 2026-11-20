# LeetCode #1210 bench, in Python: the ★ arm (a breadth-first search over
# the snake's states, its tail cell and whether it lies flat or upright) on
# 24 grids of 100 by 100 drawn once, then 40 rounds over the grids, every
# answer folded into a checksum.

seed = 1210


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_moves(grid):
    n = len(grid)

    def free(r, c):
        return r < n and c < n and grid[r][c] == 0

    dist = [-1] * (n * n * 2)
    queue = [(0, 0, 0)]
    dist[0] = 0
    head = 0
    while head < len(queue):
        r, c, up = queue[head]
        head += 1
        d = dist[(r * n + c) * 2 + up]
        if r == n - 1 and c == n - 2 and up == 0:
            return d
        nxt = []
        if up == 0:
            if free(r, c + 2):
                nxt.append((r, c + 1, 0))
            if free(r + 1, c) and free(r + 1, c + 1):
                nxt.append((r + 1, c, 0))
                nxt.append((r, c, 1))
        else:
            if free(r + 2, c):
                nxt.append((r + 1, c, 1))
            if free(r, c + 1) and free(r + 1, c + 1):
                nxt.append((r, c + 1, 1))
                nxt.append((r, c, 0))
        for nr, nc, nu in nxt:
            at = (nr * n + nc) * 2 + nu
            if dist[at] < 0:
                dist[at] = d + 1
                queue.append((nr, nc, nu))
    return -1


def random_grid(n, percent):
    grid = []
    for r in range(n):
        row = []
        for c in range(n):
            corner = (r == 0 and c < 2) or (r == n - 1 and c >= n - 2)
            row.append(1 if not corner and next_random() % 100 < percent else 0)
        grid.append(row)
    return grid


def staircase(n, s):
    grid = [[1] * n for _ in range(n)]

    def open_(r, c):
        if r < n and c < n:
            grid[r][c] = 0

    k = 0
    while k * s < n:
        at = k * s
        for c in range(at, at + s + 2):
            open_(at, c)
        for r in range(at, at + s + 2):
            open_(r, at + s)
        for d in range(4):
            open_(at + d // 2, at + d % 2)
            open_(at + d // 2, at + s + d % 2)
        k += 1
    for i in range(n):
        open_(n - 1, i)
        open_(n - 2, i)
        open_(i, n - 1)
        open_(i, n - 2)
    return grid


def main():
    grids = []
    for i in range(20):
        percent = 5 if i < 8 else 10 if i < 16 else 14
        grids.append(random_grid(100, percent))
    for s in range(3, 7):
        grids.append(staircase(100, s))
    check = 0
    for rnd in range(40):
        for grid in grids:
            check = (check * 131 + minimum_moves(grid) + 2 + rnd) % 1000000007
    print(f"40 rounds over 24 grids of 100 by 100: checksum {check}")


main()

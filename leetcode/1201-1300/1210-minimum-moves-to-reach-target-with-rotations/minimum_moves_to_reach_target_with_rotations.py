# LeetCode #1210: Minimum Moves to Reach Target with Rotations -- a Python
# mirror of the ★ arm: a breadth-first search over the snake's states, its
# tail cell and whether it lies flat or upright.


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


seed = 1210


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def show(grid):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in grid) + "]"


def main():
    cases = [
        [[0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0]],
        [[0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 1], [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 0, 0]],
        [[0, 0], [0, 0]],
        [[0, 0], [1, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        staircase(6, 3),
        staircase(10, 7),
    ]
    for grid in cases:
        print(f"{show(grid)}: {minimum_moves(grid)}")
    found = moves = check = 0
    for _ in range(1000):
        n = next_random() % 6 + 2
        percent = next_random() % 4 * 10
        grid = random_grid(n, percent)
        answer = minimum_moves(grid)
        if answer >= 0:
            found += 1
            moves += answer
        check = (check * 131 + answer + 2) % 1000000007
    print(f"1000 small grids: {found} reached, {moves} moves in all, checksum {check}")
    print(f"100 by 100, empty: {minimum_moves(random_grid(100, 0))}")
    print(f"100 by 100, a tenth blocked: {minimum_moves(random_grid(100, 10))}")
    print(f"100 by 100, a fifth blocked: {minimum_moves(random_grid(100, 20))}")
    print(f"100 by 100, a staircase of corridors: {minimum_moves(staircase(100, 4))}")


main()

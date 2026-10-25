# LeetCode #994: Rotting Oranges -- mirror of the ★ arm
# (oranges_rotting.kara), a breadth-first search from every rotten
# orange at once.
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


def random_grid(most):
    m = 1 + next_random() % most
    n = 1 + next_random() % most
    grid = []
    for _ in range(m):
        row = []
        for _ in range(n):
            k = next_random() % 16
            row.append(0 if k < 2 else (2 if k == 2 else 1))
        grid.append(row)
    return grid


def grid_text(grid):
    return "[" + ",".join("[" + ",".join(str(v) for v in row) + "]" for row in grid) + "]"


def main():
    cases = [
        [[2, 1, 1], [1, 1, 0], [0, 1, 1]],
        [[2, 1, 1], [0, 1, 1], [1, 0, 1]],
        [[0, 2]],
        [[0]],
        [[1]],
        [[2]],
        [[2, 1, 1], [1, 1, 1], [0, 1, 2]],
        [[1, 2, 1, 1, 2, 1, 1]],
        [[2], [1], [1], [1], [1]],
        [[1, 1, 0], [0, 0, 0], [0, 1, 2]],
    ]
    for grid in cases:
        print(f"grid = {grid_text(grid)} -> {oranges_rotting(grid)}")
    full = [[1] * 10 for _ in range(10)]
    corner = [row[:] for row in full]
    corner[0][0] = 2
    print(f"10 by 10, all fresh but a rotten corner: {oranges_rotting(corner)}")
    middle = [row[:] for row in full]
    middle[4][4] = 2
    print(f"10 by 10, all fresh but a rotten middle: {oranges_rotting(middle)}")
    print(f"10 by 10, all fresh: {oranges_rotting(full)}")
    snake = [[1 if r % 2 == 0 else 0 for _ in range(10)] for r in range(10)]
    for r in range(1, 10, 2):
        snake[r][9 if r % 4 == 1 else 0] = 1
    snake[0][0] = 2
    print(f"10 by 10, a winding path of 55 oranges: {oranges_rotting(snake)}")
    board = [[1 if (r + c) % 2 == 0 else 0 for c in range(10)] for r in range(10)]
    board[0][0] = 2
    print(f"10 by 10, a checkerboard: {oranges_rotting(board)}")
    for count, most in ((300, 3), (3000, 10)):
        cells = 0
        stuck = 0
        total = 0
        check = 0
        for _ in range(count):
            grid = random_grid(most)
            cells += len(grid) * len(grid[0])
            got = oranges_rotting(grid)
            if got < 0:
                stuck += 1
            else:
                total += got
            check = (check * 31 + got + 2) % 1000000007
        print(f"{count} random grids of {cells} cells: {stuck} never rot, {total} minutes, checksum {check}")


main()

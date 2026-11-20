# LeetCode #1254: Number of Closed Islands -- the Python mirror of
# closed_island.kara: each island flooded to water by recursion from its
# first cell, and counted when no cell of it reached the edge.

import sys

sys.setrecursionlimit(100000)


def closed(grid, i, j):
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
        return False
    if grid[i][j] == 1:
        return True
    grid[i][j] = 1
    up = closed(grid, i - 1, j)
    down = closed(grid, i + 1, j)
    left = closed(grid, i, j - 1)
    right = closed(grid, i, j + 1)
    return up and down and left and right


def closed_island(grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0 and closed(grid, i, j):
                count += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(m, n, land):
    return [[0 if next_random() % 100 < land else 1 for _ in range(n)] for _ in range(m)]


def main():
    global seed
    a = closed_island([[1, 1, 1, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0]])
    b = closed_island([[0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 1, 1, 0]])
    c = closed_island([[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]])
    print(a, b, c)
    seed = 1254
    total = check = 0
    for _ in range(500):
        m = next_random() % 100 + 1
        n = next_random() % 100 + 1
        land = next_random() % 61 + 20
        c = closed_island(random_grid(m, n, land))
        total += c
        check = (check * 131 + c) % 1000000007
    print(f"500 random grids: total {total}, checksum {check}")
    snake = [[1] * 100 for _ in range(100)]
    for i in range(1, 99):
        for j in range(1, 99):
            if i % 2 == 1 or (i % 4 == 2 and j == 98) or (i % 4 == 0 and j == 1):
                snake[i][j] = 0
    board = [[0 if (i + j) % 2 == 0 else 1 for j in range(100)] for i in range(100)]
    print(f"100 by 100: winding path {closed_island(snake)}, chessboard {closed_island(board)}")


main()

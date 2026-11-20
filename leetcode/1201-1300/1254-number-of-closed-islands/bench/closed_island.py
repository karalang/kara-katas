# LeetCode #1254 bench, in Python: the ★ arm (each island flooded to water
# by recursion from its first cell, and counted when no cell of it reached
# the edge) on 100 random 100 by 100 grids built once, each with its own
# share of land from 20 to 80 in 100; each copied and asked 40 times,
# every count folded into a checksum.

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


seed = 1254


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    grids = []
    for _ in range(100):
        land = next_random() % 61 + 20
        grids.append([[0 if next_random() % 100 < land else 1 for _ in range(100)] for _ in range(100)])
    check = 0
    for _ in range(40):
        for grid in grids:
            check = (check * 131 + closed_island([row[:] for row in grid])) % 1000000007
    print(f"40 rounds of 100 grids of 100 by 100: checksum {check}")


main()

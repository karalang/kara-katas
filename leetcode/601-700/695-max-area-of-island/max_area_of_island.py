# LeetCode #695: Max Area of Island -- a recursive search.
#
# A mirror of max_area_of_island.kara (the ★ arm) and its harness.
import sys

sys.setrecursionlimit(20000)


def max_area_of_island(grid):
    land = [row[:] for row in grid]
    m, n = len(land), len(land[0])

    def sink(r, c):
        if r < 0 or c < 0 or r >= m or c >= n or land[r][c] == 0:
            return 0
        land[r][c] = 0
        return 1 + sink(r + 1, c) + sink(r - 1, c) + sink(r, c + 1) + sink(r, c - 1)

    best = 0
    for r in range(m):
        for c in range(n):
            if land[r][c] == 1:
                best = max(best, sink(r, c))
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid_of(rows):
    return [[ord(ch) - 48 for ch in row] for row in rows]


def main():
    global seed
    f = max_area_of_island
    ex1 = grid_of([
        "0010000000000",
        "0000000111000",
        "0110100000000",
        "0100110010100",
        "0100110011100",
        "0000000000100",
        "0000000111000",
        "0000000110000",
    ])
    print(f"example 1: {f(ex1)}")
    print(f"example 2: {f(grid_of(['00000000']))}")
    land = [[1] * 50 for _ in range(50)]
    board = [[(r + c) % 2 for c in range(50)] for r in range(50)]
    snake = []
    for r in range(50):
        snake.append([1 if r % 2 == 0 or ((c == 49) if r % 4 == 1 else (c == 0)) else 0 for c in range(50)])
    print(f"all land: {f(land)}, checkerboard: {f(board)}, snake: {f(snake)}")
    column = grid_of(["1", "1", "1", "1", "1"])
    corner = grid_of(["110", "110", "001"])
    print(f"a column: {f(column)}, a row: {f(grid_of(['1111111']))}, corners: {f(corner)}")
    seed = 695
    total = 0
    checksum = 0
    for _ in range(200):
        m = 1 + next_random() % 50
        n = 1 + next_random() % 50
        percent = 10 + next_random() % 71
        grid = [[1 if next_random() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]
        r = f(grid)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"200 random grids: largest areas sum to {total}, checksum {checksum}")


main()

# LeetCode #694: Number of Distinct Islands -- the path of a search.
#
# A mirror of num_distinct_islands.kara (the ★ arm) and its harness.
import sys

sys.setrecursionlimit(20000)


def num_distinct_islands(grid):
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    shapes = set()

    def walk(r, c, step, path):
        if r < 0 or c < 0 or r >= m or c >= n:
            return
        if grid[r][c] == 0 or seen[r][c]:
            return
        seen[r][c] = True
        path.append(step)
        walk(r + 1, c, "d", path)
        walk(r - 1, c, "u", path)
        walk(r, c + 1, "r", path)
        walk(r, c - 1, "l", path)
        path.append("b")

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1 and not seen[r][c]:
                path = []
                walk(r, c, "s", path)
                shapes.add("".join(path))
    return len(shapes)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def grid_of(rows):
    return [[ord(ch) - 48 for ch in row] for row in rows]


def random_grid(m, n, percent):
    return [[1 if next_random() % 100 < percent else 0 for _ in range(n)] for _ in range(m)]


def main():
    global seed
    f = num_distinct_islands
    print(f"example 1: {f(grid_of(['11000', '11000', '00011', '00011']))}")
    print(f"example 2: {f(grid_of(['11011', '10000', '00001', '11011']))}")
    land = [[1] * 50 for _ in range(50)]
    board = [[(r + c) % 2 for c in range(50)] for r in range(50)]
    print(f"water: {f(grid_of(['0']))}, all land: {f(land)}, checkerboard: {f(board)}")
    mirrored = f(grid_of(["11000", "10000", "00011", "00001"]))
    turned = f(grid_of(["11000", "10000", "00001", "00011"]))
    copies = f(grid_of(["11011", "10010", "00000", "11000", "10000"]))
    print(f"an L and its mirror: {mirrored}, an L turned: {turned}, three copies: {copies}")
    seed = 694
    total = 0
    checksum = 0
    for _ in range(200):
        m = 1 + next_random() % 50
        n = 1 + next_random() % 50
        percent = 10 + next_random() % 61
        r = f(random_grid(m, n, percent))
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"200 random grids: {total} distinct islands in all, checksum {checksum}")


main()

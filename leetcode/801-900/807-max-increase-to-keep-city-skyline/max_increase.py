# LeetCode 807 -- Max Increase to Keep City Skyline: mirrors the harness
# of max_increase.kara with the ★ arm's row and column maxima.
seed = 807


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_increase_keeping_skyline(grid):
    n = len(grid)
    row_max = [0] * n
    col_max = [0] * n
    for i in range(n):
        for j in range(n):
            row_max[i] = max(row_max[i], grid[i][j])
            col_max[j] = max(col_max[j], grid[i][j])
    total = 0
    for i in range(n):
        for j in range(n):
            total += min(row_max[i], col_max[j]) - grid[i][j]
    return total


def text(grid):
    return "[" + ", ".join("[" + ", ".join(str(h) for h in row) + "]" for row in grid) + "]"


def show(grid):
    print(f"{text(grid)} -> {max_increase_keeping_skyline(grid)}")


def filled(n, h):
    return [[h] * n for _ in range(n)]


def main():
    show([[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]])
    show(filled(3, 0))
    show([[5]])
    show([[1, 2], [3, 4]])
    print(f"50 x 50 of 100 -> {max_increase_keeping_skyline(filled(50, 100))}")
    diagonal = filled(50, 0)
    for i in range(50):
        diagonal[i][i] = 100
    print(f"50 x 50 diagonal of 100 -> {max_increase_keeping_skyline(diagonal)}")
    total = 0
    check = 0
    for r in range(300):
        n = 1 + next_random() % 10
        grid = [[next_random() % 101 for _ in range(n)] for _ in range(n)]
        gain = max_increase_keeping_skyline(grid)
        total += gain
        check = (check * 131 + gain + r) % 1000000007
    print(f"300 random grids: {total} in all, checksum {check}")


main()

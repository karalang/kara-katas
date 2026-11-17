# LeetCode #2245: Maximum Trailing Zeros in a Cornered Path -- the Python
# mirror of zeros.kara: prefix sums of the twos and fives along every
# row and column, every cell tried as the corner with its row's part to
# the left or right (corner included) and its column's part above or
# below (corner left out). O(m * n).


def count_factor(value, p):
    count = 0
    while value % p == 0:
        value //= p
        count += 1
    return count


def max_trailing_zeros(grid):
    m, n = len(grid), len(grid[0])
    row_twos = [[0] * (n + 1) for _ in range(m)]
    row_fives = [[0] * (n + 1) for _ in range(m)]
    col_twos = [[0] * n for _ in range(m + 1)]
    col_fives = [[0] * n for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            t = count_factor(grid[i][j], 2)
            f = count_factor(grid[i][j], 5)
            row_twos[i][j + 1] = row_twos[i][j] + t
            row_fives[i][j + 1] = row_fives[i][j] + f
            col_twos[i + 1][j] = col_twos[i][j] + t
            col_fives[i + 1][j] = col_fives[i][j] + f
    best = 0
    for i in range(m):
        for j in range(n):
            left = (row_twos[i][j + 1], row_fives[i][j + 1])
            right = (row_twos[i][n] - row_twos[i][j], row_fives[i][n] - row_fives[i][j])
            up = (col_twos[i][j], col_fives[i][j])
            down = (col_twos[m][j] - col_twos[i + 1][j], col_fives[m][j] - col_fives[i + 1][j])
            for ht, hf in (left, right):
                for vt, vf in (up, down):
                    best = max(best, min(ht + vt, hf + vf))
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_grid(rows, cols, top):
    return [[next_random() % top + 1 for _ in range(cols)] for _ in range(rows)]


def show(grid):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid) + "]"


def main():
    global seed
    examples = [
        [[23, 17, 15, 3, 20], [8, 1, 20, 27, 11], [9, 4, 6, 2, 21], [40, 9, 1, 10, 6], [22, 7, 4, 5, 3]],
        [[4, 3, 2], [7, 6, 1], [8, 8, 8]],
        [[10]],
        [[2, 5, 10, 1000]],
        [[25], [4], [1]],
        [[1, 125, 1], [1, 1, 1], [8, 1, 1]],
    ]
    for grid in examples:
        print(f"{show(grid)} -> {max_trailing_zeros(grid)}")
    seed = 2245
    check = 0
    most = 0
    for _ in range(2000):
        rows = next_random() % 8 + 1
        cols = next_random() % 8 + 1
        grid = random_grid(rows, cols, 50)
        zeros = max_trailing_zeros(grid)
        most = max(most, zeros)
        check = (check * 31 + zeros + 1) % 1000000007
    print(f"2000 grids: most {most}, checksum {check}")
    grid = random_grid(250, 400, 1000)
    print(f"250 x 400: {max_trailing_zeros(grid)}")
    grid = random_grid(1, 100000, 1000)
    print(f"1 x 100000: {max_trailing_zeros(grid)}")


main()

# LeetCode #2245: Maximum Trailing Zeros in a Cornered Path -- the
# benchmark's Python mirror of zeros.kara: prefix sums of the twos and
# fives of each row and column, every cell tried as the corner.


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


seed = 2245


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(40):
        grid = [[next_random() % 1000 + 1 for _ in range(400)] for _ in range(250)]
        check = (check * 31 + max_trailing_zeros(grid) + 1) % 1000000007
    print(f"40 grids of 250 x 400: checksum {check}")


main()

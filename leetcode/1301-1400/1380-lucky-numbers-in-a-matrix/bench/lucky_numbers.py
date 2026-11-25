# LeetCode #1380 bench -- Python: the ★ arm: each row's least value and
# each column's greatest found in one pass, then every cell that is both.


def lucky_numbers(matrix):
    m, n = len(matrix), len(matrix[0])
    row_min = [2**31 - 1] * m
    col_max = [-(2**31)] * n
    for i in range(m):
        for j in range(n):
            row_min[i] = min(row_min[i], matrix[i][j])
            col_max[j] = max(col_max[j], matrix[i][j])
    lucky = []
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == row_min[i] and matrix[i][j] == col_max[j]:
                lucky.append(matrix[i][j])
    return lucky


seed = 1380


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 20 matrices of 50 by 50 built once; then 20000 rounds, each swapping
    # two cells of one matrix and finding its lucky numbers (see the Kāra
    # bench)
    n = 50
    grids = []
    for _ in range(20):
        grid = [[i * n + j + 1 for j in range(n)] for i in range(n)]
        for _ in range(300):
            a = next_random() % (n * n)
            b = next_random() % (n * n)
            grid[a // n][a % n], grid[b // n][b % n] = grid[b // n][b % n], grid[a // n][a % n]
        grids.append(grid)
    check = 0
    for r in range(20000):
        grid = grids[check % 20]
        a = (check // 20) % (n * n)
        b = (check // 7 + r) % (n * n)
        grid[a // n][a % n], grid[b // n][b % n] = grid[b // n][b % n], grid[a // n][a % n]
        lucky = lucky_numbers(grid)
        got = len(lucky)
        for v in lucky:
            got = got * 2503 + v
        check = (check * 31 + got + r) % 1000000007
    print(f"20000 rounds over 20 matrices of 50 by 50: checksum {check}")


main()

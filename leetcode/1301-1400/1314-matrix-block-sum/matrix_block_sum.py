# LeetCode #1314: Matrix Block Sum -- Python mirror of the ★ arm: a table of
# sums over every top-left rectangle, each block's sum four lookups.


def matrix_block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    sums = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            sums[i + 1][j + 1] = mat[i][j] + sums[i][j + 1] + sums[i + 1][j] - sums[i][j]
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        top, bottom = max(i - k, 0), min(i + k + 1, m)
        for j in range(n):
            left, right = max(j - k, 0), min(j + k + 1, n)
            out[i][j] = sums[bottom][right] - sums[top][right] - sums[bottom][left] + sums[top][left]
    return out


seed = 1314


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(grid):
    return "/".join(",".join(str(x) for x in row) for row in grid)


def main():
    three = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    e1 = matrix_block_sum(three, 1)
    e2 = matrix_block_sum(three, 2)
    one = matrix_block_sum([[5]], 3)
    row = matrix_block_sum([[1, 2, 3, 4, 5]], 1)
    column = matrix_block_sum([[1], [2], [3], [4]], 2)
    print(f"{show(e1)} {show(e2)} {show(one)} {show(row)} {show(column)}")
    total = 0
    check = 0
    for _ in range(600):
        m = 1 + next_random() % 100
        n = 1 + next_random() % 100
        if next_random() % 4 == 0:
            k = 1 + next_random() % 100
        else:
            k = 1 + next_random() % 5
        mat = [[1 + next_random() % 100 for _ in range(n)] for _ in range(m)]
        for r in matrix_block_sum(mat, k):
            for x in r:
                total += x
                check = (check * 31 + x) % 1000000007
    print(f"600 random matrices: sum of answers {total}, checksum {check}")


main()

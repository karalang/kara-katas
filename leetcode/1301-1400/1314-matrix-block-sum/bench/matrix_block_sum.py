# LeetCode #1314 bench, Python: the ★ arm (a table of sums over every
# top-left rectangle, each block's sum four lookups) on the same 20 matrices
# and 200 passes.


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


def main():
    n = 100
    mats = [[[1 + next_random() % 100 for _ in range(n)] for _ in range(n)] for _ in range(20)]
    check = 0
    for p in range(200):
        for g in range(20):
            mats[g][check % n][(check // 7) % n] = 1 + (check // 11) % 100
            k = 1 + (check // 13) % 100 if check % 4 == 0 else 1 + (check // 13) % 5
            got = matrix_block_sum(mats[g], k)
            check = (check * 31 + got[(check // 3) % n][(check // 17) % n]) % 1000000007
            check = (check * 31 + got[(check // 19) % n][(check // 23) % n] + p) % 1000000007
    print(f"200 passes over 20 matrices of 100 by 100: checksum {check}")


main()

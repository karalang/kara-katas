# LeetCode #1292 bench: the ★ arm over 20 matrices of 300 by 300 with values
# up to 100, built once; then 100 passes, each setting one cell of every
# matrix and its threshold from the checksum so far and answering it.


def max_side_length(mat, threshold):
    m, n = len(mat), len(mat[0])
    s = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        row, above = s[i], s[i - 1]
        src = mat[i - 1]
        for j in range(1, n + 1):
            row[j] = src[j - 1] + above[j] + row[j - 1] - above[j - 1]
            k = best + 1
            if i >= k and j >= k and row[j] - s[i - k][j] - row[j - k] + s[i - k][j - k] <= threshold:
                best = k
    return best


def main():
    seed = 1292

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    mats = [[[next_random() % 101 for _ in range(300)] for _ in range(300)] for _ in range(20)]
    check = 0
    for p in range(100):
        for a in range(len(mats)):
            mats[a][check % 300][(check // 300) % 300] = check % 101
            threshold = check % 100001
            check = (check * 31 + max_side_length(mats[a], threshold) + p) % 1000000007
    print(f"100 passes over 20 matrices of 300 by 300: checksum {check}")


main()

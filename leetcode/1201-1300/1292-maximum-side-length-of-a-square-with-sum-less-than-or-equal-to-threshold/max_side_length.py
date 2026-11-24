# LeetCode #1292: Maximum Side Length of a Square with Sum Less than or Equal
# to Threshold -- Python mirror of the ★ arm: prefix sums, each corner trying
# a square one longer than the best so far.


def max_side_length(mat, threshold):
    m, n = len(mat), len(mat[0])
    s = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s[i][j] = mat[i - 1][j - 1] + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1]
            k = best + 1
            if i >= k and j >= k and s[i][j] - s[i - k][j] - s[i][j - k] + s[i - k][j - k] <= threshold:
                best = k
    return best


def main():
    seed = 1292

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide_random():
        a = next_random()
        return a * 32768 + next_random()

    def problem(m, n, top):
        return [[wide_random() % (top + 1) for _ in range(n)] for _ in range(m)]

    ex1 = [[1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2]]
    ex2 = [[2] * 5 for _ in range(5)]
    print(f"{max_side_length(ex1, 4)} {max_side_length(ex2, 1)} {max_side_length([[0, 0], [0, 0]], 0)} {max_side_length([[1, 1], [1, 1]], 0)} {max_side_length([[7]], 7)} {max_side_length([[7]], 6)}")
    total = 0
    check = 0
    for k in range(601):
        top = 9 if k == 600 else [10000, 100, 9][k % 3]
        m = 100 if k == 600 else next_random() % 30 + 1
        n = 100 if k == 600 else next_random() % 30 + 1
        mat = problem(m, n, top)
        threshold = wide_random() % 100001
        side = max_side_length(mat, threshold)
        total += side
        check = (check * 131 + side) % 1000000007
    print(f"601 random matrices: sides total {total}, checksum {check}")


main()

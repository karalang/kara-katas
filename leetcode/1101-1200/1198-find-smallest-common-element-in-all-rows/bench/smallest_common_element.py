# LeetCode #1198 bench: the ★ arm in Python, over the same 20 matrices of
# 500 x 500 and 100 rounds as the Kāra bench.

ROUNDS = 100


def smallest_common_element(mat):
    count = [0] * 10001
    for row in mat:
        for v in row:
            count[v] += 1
    for v in mat[0]:
        if count[v] == len(mat):
            return v
    return -1


def main():
    seed = 1198

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def random_row(n, high):
        row = []
        v = 0
        while len(row) < n:
            v += 1 + next_random() % (2 * high // n)
            if v > high - (n - len(row)) + 1:
                v = high - (n - len(row)) + 1
            row.append(v)
        return row

    highs = [520, 1000, 5000, 10000]
    mats = [[random_row(500, highs[k % 4]) for _ in range(500)] for k in range(20)]
    check = 0
    for _ in range(ROUNDS):
        for mat in mats:
            v = smallest_common_element(mat)
            check = (check * 131 + v + 2) % 1000000007
    print(f"{ROUNDS} rounds of 20 matrices of 500 x 500: checksum {check}")


main()

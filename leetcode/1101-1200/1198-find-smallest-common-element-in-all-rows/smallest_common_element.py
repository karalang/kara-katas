# LeetCode #1198: Find Smallest Common Element in All Rows -- the ★ arm in
# Python: a count of each value over the whole matrix, and the first value
# of the first row counted once in every row.


def smallest_common_element(mat):
    count = [0] * 10001
    for row in mat:
        for v in row:
            count[v] += 1
    for v in mat[0]:
        if count[v] == len(mat):
            return v
    return -1


# ---- test harness ---------------------------------------------------------

seed = 1198


def next_random():
    global seed
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


def show(mat):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in mat) + "]"


def main():
    cases = [
        [[1, 2, 3, 4, 5], [2, 4, 5, 8, 10], [3, 5, 7, 9, 11], [1, 3, 5, 7, 9]],
        [[1, 2, 3], [2, 3, 4], [2, 3, 5]],
        [[1, 2, 3], [4, 5, 6]],
        [[7]],
        [[1, 10000], [10000]],
        [[1, 3, 5], [2, 3, 5], [3, 4, 5]],
    ]
    for c in cases:
        print(f"{show(c)}: {smallest_common_element(c)}")
    print(f"one row of 500: {smallest_common_element([list(range(1, 501))])}")
    found = 0
    check = 0
    for _ in range(1000):
        m = next_random() % 6 + 1
        n = next_random() % 12 + 1
        high = n + next_random() % 30
        mat = [random_row(n, high) for _ in range(m)]
        v = smallest_common_element(mat)
        if v >= 0:
            found += 1
        check = (check * 131 + v + 2) % 1000000007
    print(f"1000 random matrices: {found} with a common element, checksum {check}")
    big = [random_row(500, 10000) for _ in range(500)]
    print(f"500 rows of 500 from 1 to 10000: {smallest_common_element(big)}")
    dense = [random_row(500, 520) for _ in range(500)]
    print(f"500 rows of 500 from 1 to 520: {smallest_common_element(dense)}")


main()

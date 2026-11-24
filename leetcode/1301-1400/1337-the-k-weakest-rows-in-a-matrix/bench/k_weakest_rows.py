# LeetCode #1337 bench, Python mirror of the Kāra bench: the ★ arm on 50
# matrices of 100 by 100 built once, then 2000 passes, each rewriting one
# row of every matrix and choosing k from the checksum so far, answering
# every matrix.


def soldiers(row):
    low, high = 0, len(row)
    while low < high:
        mid = (low + high) // 2
        if row[mid] == 1:
            low = mid + 1
        else:
            high = mid
    return low


def k_weakest_rows(mat, k):
    rows = sorted((soldiers(row), i) for i, row in enumerate(mat))
    return [i for _, i in rows[:k]]


seed = 1337


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 100
    mats = []
    for _ in range(50):
        mat = []
        for _ in range(n):
            s = next_random() % (n + 1)
            mat.append([1] * s + [0] * (n - s))
        mats.append(mat)
    check = 0
    for p in range(2000):
        k = 1 + check % n
        for t in range(50):
            r = check % n
            s = check // 7 % (n + 1)
            row = mats[t][r]
            for c in range(n):
                row[c] = 1 if c < s else 0
            rows = k_weakest_rows(mats[t], k)
            check = (check * 31 + rows[0] + rows[-1] + p) % 1000000007
    print(f"2000 passes over 50 matrices of 100 by 100: checksum {check}")


main()

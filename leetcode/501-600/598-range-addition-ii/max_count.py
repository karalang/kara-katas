# LeetCode #598: Range Addition II -- the smallest corner.
#
# Mirrors max_count.kara: the cells at the maximum are the rows below the
# smallest a and the columns below the smallest b.


def max_count(m, n, ops):
    rows = m
    cols = n
    for op in ops:
        rows = min(rows, op[0])
        cols = min(cols, op[1])
    return rows * cols


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(m, n, ops):
    print(f"m = {m}, n = {n}, ops = {ops} -> {max_count(m, n, ops)}")


def main():
    show(3, 3, [[2, 2], [3, 3]])
    many = [[2, 2] if k % 4 == 0 else [3, 3] for k in range(12)]
    show(3, 3, many)
    show(3, 3, [])
    show(1, 1, [[1, 1]])
    show(4, 5, [[4, 5]])
    show(1, 6, [[1, 4], [1, 6]])
    show(5, 5, [[2, 5], [5, 3], [4, 4]])
    show(40000, 40000, [])
    seed = [598]
    big = []
    for _ in range(10000):
        a = 30000 + step(seed) % 10001
        b = 20000 + step(seed) % 20001
        big.append([a, b])
    print(f"10000 operations on 40000 x 40000 -> {max_count(40000, 40000, big)}")
    total = 0
    checksum = 0
    for _ in range(300):
        m = 1 + step(seed) % 30
        n = 1 + step(seed) % 30
        k = step(seed) % 13
        ops = []
        for _ in range(k):
            a = 1 + step(seed) % m
            b = 1 + step(seed) % n
            ops.append([a, b])
        got = max_count(m, n, ops)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")


main()

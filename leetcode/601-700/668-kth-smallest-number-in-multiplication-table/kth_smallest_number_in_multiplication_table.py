# LeetCode #668: Kth Smallest Number in Multiplication Table -- binary
# search on the value, counting by rows.
# Mirrors the ★ arm (kth_smallest_number_in_multiplication_table.kara)
# and its test harness.


def find_kth_number(m, n, k):
    lo, hi = 1, m * n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        count = 0
        for i in range(1, m + 1):
            count += min(mid // i, n)
        if count >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(m, n, k):
    print(f"m={m} n={n} k={k}: {find_kth_number(m, n, k)}")


def main():
    for m, n, k in [(3, 3, 5), (2, 3, 6), (1, 1, 1), (4, 5, 1), (4, 5, 20), (1, 9, 7),
                    (9, 1, 7), (20, 3, 31), (3, 20, 31), (12, 12, 72),
                    (30000, 30000, 1), (30000, 30000, 450000000), (30000, 30000, 900000000),
                    (30000, 30000, 123456789), (30000, 17, 400000), (17, 30000, 400000)]:
        show(m, n, k)
    print("6 by 7: " + ",".join(str(find_kth_number(6, 7, k)) for k in range(1, 43)))
    rng = Rng(668)
    s = 0
    for _ in range(1000):
        m = 1 + rng.next() % 40
        n = 1 + rng.next() % 40
        k = 1 + rng.next() % (m * n)
        s = (s * 31 + find_kth_number(m, n, k)) % 1000000007
    print(f"1000 random tables: checksum {s}")


main()

# Benchmark for #668: binary search on the value, counting by rows, as
# the Kara ★ arm.


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


def main():
    rounds = 200
    s = 0
    for r in range(rounds):
        m = 30000 - r * 97 % 10000
        n = 30000 - r * 89 % 10000
        k = 1 + r * 7919813 % (m * n)
        s = (s * 31 + find_kth_number(m, n, k)) % 1000000007
    print(f"{rounds} rounds: checksum {s}")


main()

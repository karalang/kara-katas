# LeetCode #1802: Maximum Value at a Given Index in a Bounded Array -- the
# bench in Python: the ★ arm over 4000 random cases built once, 1000000
# calls.


def side(v, k):
    if k <= v - 1:
        return (v - 1 + v - k) * k // 2
    return (v - 1) * v // 2 + (k - (v - 1))


def max_value(n, index, max_sum):
    lo, hi = 1, max_sum
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid + side(mid, index) + side(mid, n - 1 - index) <= max_sum:
            lo = mid
        else:
            hi = mid - 1
    return lo


seed = 1802


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(4000):
        n = 1 + next_random() % 1000000
        index = next_random() % n
        hi = next_random()
        wide = hi * 32768 + next_random()
        cases.append((n, index, n + wide % (1000000001 - n)))
    check = 0
    for call in range(1000000):
        n, index, max_sum = cases[(check + call) % 4000]
        check = (check * 31 + max_value(n, index, max_sum)) % 1000000007
    print(f"1000000 calls over 4000 cases: checksum {check}")


main()

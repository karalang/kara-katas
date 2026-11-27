# LeetCode #1802: Maximum Value at a Given Index in a Bounded Array -- the
# ★ arm in Python: a binary search on the value at `index`.


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
    print(f"{max_value(4, 2, 6)} {max_value(6, 1, 10)}")
    print(f"{max_value(1, 0, 7)} {max_value(5, 2, 5)} {max_value(5, 2, 6)} {max_value(5, 0, 15)} {max_value(5, 4, 15)} {max_value(5, 2, 9)}")
    print(f"the most: {max_value(1, 0, 1000000000)} {max_value(1000000000, 0, 1000000000)} {max_value(100000, 50000, 1000000000)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        index = next_random() % n
        max_sum = n + next_random() % 400
        check = (check * 31 + max_value(n, index, max_sum)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()

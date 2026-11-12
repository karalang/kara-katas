# LeetCode #1131: Maximum of Absolute Value Expression -- the Python mirror
# of the ★ arm: each of the four sign pairs (p, q) gives every index the
# value p * arr1[i] + q * arr2[i] + i, and the answer is the widest spread
# of those values under any pair.


def max_abs_val_expr(arr1, arr2):
    best = 0
    for p, q in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        hi = None
        lo = None
        for i in range(len(arr1)):
            v = p * arr1[i] + q * arr2[i] + i
            if hi is None or v > hi:
                hi = v
            if lo is None or v < lo:
                lo = v
        best = max(best, hi - lo)
    return best


seed = 1131


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def value():
    return (next_random() * 32768 + next_random()) % 2000001 - 1000000


def main():
    cases = [
        ([1, 2, 3, 4], [-1, 4, 5, 6]),
        ([1, -2, -5, 0, 10], [0, -2, -1, -7, -4]),
        ([0, 0], [0, 0]),
        ([7, 7, 7, 7, 7, 7], [3, 3, 3, 3, 3, 3]),
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([-1000000, 1000000], [1000000, -1000000]),
        ([5, -5, 5, -5], [-5, 5, -5, 5]),
        ([3, 1, 4, 1, 5, 9, 2, 6], [2, 7, 1, 8, 2, 8, 1, 8]),
    ]
    for a, b in cases:
        print(f"{a}, {b} -> {max_abs_val_expr(a, b)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 59 + 2
        a = [value() for _ in range(n)]
        b = [value() for _ in range(n)]
        r = max_abs_val_expr(a, b)
        total += r
        check = (check * 31 + r) % 1000000007
    print(f"2000 random pairs: answers total {total}, checksum {check}")
    a = [value() for _ in range(40000)]
    b = [value() for _ in range(40000)]
    print(f"40000 random values each: {max_abs_val_expr(a, b)}")
    print(f"40000 rising against falling: {max_abs_val_expr(list(range(40000)), [-i for i in range(40000)])}")


main()

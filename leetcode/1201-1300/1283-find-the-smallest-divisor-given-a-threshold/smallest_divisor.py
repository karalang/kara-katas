# LeetCode #1283: Find the Smallest Divisor Given a Threshold -- Python
# mirror of the ★ arm: a binary search over 1 to the largest number for
# the first divisor whose sum of rounded-up quotients is within the
# threshold.


def total(nums, d):
    s = 0
    for x in nums:
        s += (x + d - 1) // d
    return s


def smallest_divisor(nums, threshold):
    lo = 1
    hi = max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if total(nums, mid) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, top):
    out = []
    for _ in range(n):
        hi = next_random()
        out.append(1 + (hi * 32768 + next_random()) % top)
    return out


def main():
    global seed
    shown = [
        smallest_divisor([1, 2, 5, 9], 6),
        smallest_divisor([44, 22, 33, 11, 1], 5),
        smallest_divisor([21212, 10101, 12121], 1000000),
        smallest_divisor([2, 3, 5, 7, 11], 11),
    ]
    print(" ".join(str(d) for d in shown))
    seed = 1283
    big = drawn(50000, 1000000)
    at = [str(smallest_divisor(big, t)) for t in [50000, 100000, 1000000]]
    print(f"5 * 10^4 numbers: {' '.join(at)}")
    check = 0
    tot = 0
    for i in range(2000):
        n = 1 + next_random() % 30
        top = 10 if i % 3 == 0 else (1000 if i % 3 == 1 else 1000000)
        nums = drawn(n, top)
        threshold = n + next_random() % 101 if i % 2 == 0 else n + next_random() % (1000001 - n)
        d = smallest_divisor(nums, threshold)
        tot += d
        check = (check * 131 + d) % 1000000007
    print(f"2000 random cases: {tot} in all, checksum {check}")


main()

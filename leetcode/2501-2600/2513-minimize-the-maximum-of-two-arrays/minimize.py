# LeetCode #2513: Minimize the Maximum of Two Arrays -- Python mirror of
# the ★ arm (minimize.kara): the least x whose three counts reach their
# needs, by binary search, and its harness, line for line.
from math import gcd


def minimize_set(divisor1, divisor2, unique_cnt1, unique_cnt2):
    lcm = divisor1 // gcd(divisor1, divisor2) * divisor2

    def enough(x):
        return (x - x // divisor1 >= unique_cnt1 and x - x // divisor2 >= unique_cnt2
                and x - x // lcm >= unique_cnt1 + unique_cnt2)

    lo, hi = 1, 2 * (unique_cnt1 + unique_cnt2)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if enough(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def main():
    global seed
    cases = [(2, 7, 1, 3), (3, 5, 2, 1), (2, 4, 8, 2), (2, 2, 1, 1), (2, 3, 1, 1),
             (100000, 100000, 1, 1), (2, 2, 500000000, 500000000), (99991, 99989, 999999999, 1)]
    for d1, d2, c1, c2 in cases:
        print(f"{d1} {d2} {c1} {c2} -> {minimize_set(d1, d2, c1, c2)}")
    seed = 2513
    for top, most in [(10, 50), (100000, 1000000000)]:
        total = 0
        check = 0
        for _ in range(2000):
            d1 = below(top - 1) + 2
            d2 = below(top - 1) + 2
            c1 = below(most - 1) + 1
            c2 = below(most - c1) + 1
            a = minimize_set(d1, d2, c1, c2)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"2000 random, divisors to {top}: total {total}, checksum {check}")
    for d1, d2 in [(2, 3), (2, 4), (99999, 100000), (100000, 100000)]:
        check = 0
        for s in range(1, 10):
            check = (check * 31 + minimize_set(d1, d2, s * 100000000, 1000000000 - s * 100000000)) % 1000000007
        print(f"10^9 split nine ways, divisors {d1} and {d2}: checksum {check}")


main()

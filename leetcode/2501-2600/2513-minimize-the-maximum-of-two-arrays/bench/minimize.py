# LeetCode #2513: Minimize the Maximum of Two Arrays -- benchmark mirror
# of the ★ arm (minimize.kara): 10^5 cases built once from its own
# generator, then the passes; each asks every case with its first count
# raised by the checksum so far, mod 1000.
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


seed = 2513


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def main():
    cases = []
    for _ in range(100000):
        d1 = below(99999) + 2
        d2 = below(99999) + 2
        c1 = below(999998999) + 1
        c2 = below(999999000 - c1) + 1
        cases.append((d1, d2, c1, c2))
    passes = 10
    check = 0
    for p in range(passes):
        for d1, d2, c1, c2 in cases:
            check = (check * 31 + minimize_set(d1, d2, c1 + check % 1000, c2) + p) % 1000000007
    print(f"{passes} passes over 10^5 cases: checksum {check}")


main()

# LeetCode #1201: Ugly Number III -- the ★ arm in Python: a binary search
# on the answer, the numbers up to x divisible by a, b or c counted by
# inclusion and exclusion over the least common multiples.

from math import gcd


def lcm(a, b):
    return a // gcd(a, b) * b


def nth_ugly_number(n, a, b, c):
    ab, bc, ac = lcm(a, b), lcm(b, c), lcm(a, c)
    abc = lcm(ab, c)

    def count(x):
        return x // a + x // b + x // c - x // ab - x // bc - x // ac + x // abc

    low, high = 1, n * min(a, b, c)
    while low < high:
        mid = low + (high - low) // 2
        if count(mid) >= n:
            high = mid
        else:
            low = mid + 1
    return low


# ---- test harness ---------------------------------------------------------

seed = 1201


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    high = next_random()
    low = next_random()
    return high * 32768 + low


cases = [
    (3, 2, 3, 5),
    (4, 2, 3, 4),
    (5, 2, 11, 13),
    (1000000000, 2, 217983653, 336916467),
    (1, 1, 1, 1),
    (1000000000, 1, 1, 1),
    (1000000000, 2, 2, 2),
    (5, 2, 4, 8),
    (2, 1000000, 1000000, 1000000),
    (2, 999999937, 999999929, 1),
    (7, 6, 10, 15),
]
for n, a, b, c in cases:
    print(f"n = {n}, a = {a}, b = {b}, c = {c}: {nth_ugly_number(n, a, b, c)}")
total = check = 0
for _ in range(1000):
    a = next_random() % 30 + 1
    b = next_random() % 30 + 1
    c = next_random() % 30 + 1
    n = next_random() % 200 + 1
    v = nth_ugly_number(n, a, b, c)
    total += v
    check = (check * 131 + v) % 1000000007
print(f"1000 small cases: total {total}, checksum {check}")
total = check = 0
for _ in range(1000):
    a = big() % 1000000 + 1
    b = big() % 1000000 + 1
    c = big() % 1000000 + 1
    most = 2000000000 // min(a, b, c)
    n = big() % min(most, 1000000000) + 1
    v = nth_ugly_number(n, a, b, c)
    total += v
    check = (check * 131 + v) % 1000000007
print(f"1000 large cases: total {total}, checksum {check}")

# LeetCode #1201 bench: the ★ arm in Python, over the same 50000 queries
# and 10 rounds as the Kāra bench.

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


seed = 1201


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    high = next_random()
    low = next_random()
    return high * 32768 + low


tops = [1000000, 1000, 30]
queries = []
for k in range(50000):
    top = tops[k % 3]
    a = big() % top + 1
    b = big() % top + 1
    c = big() % top + 1
    most = min(2000000000 // min(a, b, c), 1000000000)
    n = big() % most + 1
    queries.append((n, a, b, c))
check = 0
for _ in range(10):
    for n, a, b, c in queries:
        check = (check * 131 + nth_ugly_number(n, a, b, c)) % 1000000007
print(f"10 rounds of 50000 queries: checksum {check}")

"""Benchmark workload for LeetCode #263 — Ugly Number (Python mirror).

Mirrors ugly_sweep.kara algorithm-for-algorithm. Correctness oracle only —
Python is not a measured lane (see BENCHMARKS.md).
"""

I64_MAX = 9223372036854775807


def gcd(a, b):
    x, y = a, b
    while y != 0:
        x, y = y, x % y
    return x


def is_ugly(n):
    if n <= 0:
        return False
    m = n
    g = gcd(m, 30)
    while g > 1:
        m //= g
        g = gcd(m, 30)
    return m == 1


def main():
    n = 10000000
    limit = I64_MAX

    ring = []
    rs = 7717
    for _ in range(64):
        v = 1
        steps = 0
        while steps < 40:
            rs = (rs * 1103515245 + 12345) & 2147483647
            pick = (rs // 65536) % 3
            f = 3 if pick == 1 else (5 if pick == 2 else 2)
            if v <= limit // f:
                v *= f
            else:
                steps = 40
            steps += 1
        ring.append(v)

    state = 263263
    uglies = 0
    digest = 0
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        hi = state
        state = (state * 1103515245 + 12345) & 2147483647
        probe = hi * 2147483648 + state
        if i % 512 == 0:
            probe = ring[(i // 512) % 64]
        bit = 0
        if is_ugly(probe):
            uglies += 1
            bit = 1
        digest = (digest * 131 + bit * 7 + probe % 1000003) % 1000000007

    print(uglies)
    print(digest)


main()

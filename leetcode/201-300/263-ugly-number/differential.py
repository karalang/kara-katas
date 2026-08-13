"""LeetCode 263 — differential harness (Python mirror / oracle).

Mirrors differential.kara draw-for-draw: the same LCG, the same order of seed
advances, the same four families, so the printed digest must match byte for
byte.
"""

MASK = 2147483647
I64_MAX = 9223372036854775807
DIGEST_MOD = 1000000007


def is_ugly_div(n):
    if n <= 0:
        return False
    m = n
    while m % 2 == 0:
        m //= 2
    while m % 3 == 0:
        m //= 3
    while m % 5 == 0:
        m //= 5
    return m == 1


def gcd(a, b):
    x, y = a, b
    while y != 0:
        x, y = y, x % y
    return x


def is_ugly_gcd(n):
    if n <= 0:
        return False
    m = n
    g = gcd(m, 30)
    while g > 1:
        m //= g
        g = gcd(m, 30)
    return m == 1


def is_ugly_enum(n):
    if n <= 0:
        return False
    if n == 1:
        return True
    u = [1]
    i2 = i3 = i5 = 0
    while True:
        has2 = u[i2] <= n // 2
        c2 = u[i2] * 2 if has2 else 0
        has3 = u[i3] <= n // 3
        c3 = u[i3] * 3 if has3 else 0
        has5 = u[i5] <= n // 5
        c5 = u[i5] * 5 if has5 else 0
        if not has2 and not has3 and not has5:
            return False
        nxt = None
        if has2:
            nxt = c2
        if has3 and (nxt is None or c3 < nxt):
            nxt = c3
        if has5 and (nxt is None or c5 < nxt):
            nxt = c5
        if nxt == n:
            return True
        u.append(nxt)
        if has2 and c2 == nxt:
            i2 += 1
        if has3 and c3 == nxt:
            i3 += 1
        if has5 and c5 == nxt:
            i5 += 1


def ugly_table(limit):
    mark = [False] * (limit + 1)
    u = [1]
    mark[1] = True
    i2 = i3 = i5 = 0
    while True:
        has2 = u[i2] <= limit // 2
        c2 = u[i2] * 2 if has2 else 0
        has3 = u[i3] <= limit // 3
        c3 = u[i3] * 3 if has3 else 0
        has5 = u[i5] <= limit // 5
        c5 = u[i5] * 5 if has5 else 0
        if not has2 and not has3 and not has5:
            break
        nxt = None
        if has2:
            nxt = c2
        if has3 and (nxt is None or c3 < nxt):
            nxt = c3
        if has5 and (nxt is None or c5 < nxt):
            nxt = c5
        u.append(nxt)
        mark[nxt] = True
        if has2 and c2 == nxt:
            i2 += 1
        if has3 and c3 == nxt:
            i3 += 1
        if has5 and c5 == nxt:
            i5 += 1
    return mark


def main():
    mismatches = 0
    uglies = 0
    checked = 0
    digest = 0

    band = 20000
    mark = ugly_table(band)
    for n in range(-100, band + 1):
        a = is_ugly_div(n)
        b = is_ugly_gcd(n)
        c = mark[n] if n > 0 else False
        if a != b or a != c:
            mismatches += 1
        if a:
            uglies += 1
        digest = (digest * 131 + (1 if a else 0)) % DIGEST_MOD
        checked += 1
    exhaustive_uglies = uglies

    limit = I64_MAX
    seed = 263263
    big_ugly = 0
    near_miss = 0

    for _ in range(600):
        seed = (seed * 1103515245 + 12345) & MASK
        family = (seed // 65536) % 3

        v = 1
        steps = 0
        seed = (seed * 1103515245 + 12345) & MASK
        want = (seed // 65536) % 13
        if (seed // 65536) % 8 == 0:
            want = (seed // 65536) % 90
        while steps < want:
            seed = (seed * 1103515245 + 12345) & MASK
            pick = (seed // 65536) % 3
            f = 2 if pick == 0 else (3 if pick == 1 else 5)
            if v <= limit // f:
                v = v * f
            else:
                steps = want
            steps += 1

        probe = v
        if family == 1:
            seed = (seed * 1103515245 + 12345) & MASK
            pick = (seed // 65536) % 5
            q = (7, 11, 13, 17, 9973)[pick]
            probe = v * q if v <= limit // q else q
        if family == 2:
            seed = (seed * 1103515245 + 12345) & MASK
            seed = (seed * 1103515245 + 12345) & MASK
            probe = seed

        a = is_ugly_div(probe)
        b = is_ugly_gcd(probe)
        d = is_ugly_enum(probe)
        if a != b or a != d:
            mismatches += 1
        if a:
            uglies += 1
        if family == 0 and a:
            big_ugly += 1
        if family == 1 and not a:
            near_miss += 1
        digest = (digest * 131 + (1 if a else 0) * 7 + probe % 97) % DIGEST_MOD
        checked += 1

    print(f"checked {checked}")
    print(f"ugly {uglies}")
    print(f"ugly in [-100,20000] {exhaustive_uglies}")
    print(f"constructed ugly confirmed {big_ugly}")
    print(f"near-misses rejected {near_miss}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


main()

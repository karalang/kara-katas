"""Benchmark workload for LeetCode #248 — Strobogrammatic Number III (Python; scale lane)."""

PAIR_A = ["0", "1", "6", "8", "9"]
PAIR_B = ["0", "1", "9", "8", "6"]


def pow5(e):
    a = 1
    for _ in range(e):
        a *= 5
    return a


def count_of_length(l):
    if l <= 0:
        return 0
    if l == 1:
        return 3
    t = 4 * pow5(l // 2 - 1)
    if l % 2 == 1:
        t *= 3
    return t


def build(k, n):
    if k == 0:
        return [""]
    if k == 1:
        return ["0", "1", "8"]
    out = []
    for s in build(k - 2, n):
        for p in range(5):
            if PAIR_A[p] == "0" and k == n:
                continue
            out.append(PAIR_A[p] + s + PAIR_B[p])
    return out


def cmp_digits(a, b):
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for i in range(len(a)):
        if a[i] != b[i]:
            return -1 if a[i] < b[i] else 1
    return 0


def count_bounded(l, low, high, use_lo, use_hi):
    n = 0
    for s in build(l, l):
        keep = True
        if use_lo and cmp_digits(s, low) < 0:
            keep = False
        if use_hi and cmp_digits(s, high) > 0:
            keep = False
        if keep:
            n += 1
    return n


def count_in_range(low, high):
    ll, hl = len(low), len(high)
    if ll > hl:
        return 0
    if ll == hl:
        if cmp_digits(low, high) > 0:
            return 0
        return count_bounded(ll, low, high, True, True)
    total = count_bounded(ll, low, high, True, False)
    total += count_bounded(hl, low, high, False, True)
    for l in range(ll + 1, hl):
        total += count_of_length(l)
    return total


def main():
    queries = 1000
    state = 248248
    sink = 0
    for _ in range(queries):
        state = (state * 1103515245 + 12345) & 2147483647
        da = (state // 65536) % 8 + 1
        state = (state * 1103515245 + 12345) & 2147483647
        db = (state // 65536) % 8 + 1
        state = (state * 1103515245 + 12345) & 2147483647
        ra = (state // 65536) % 9000 + 1
        state = (state * 1103515245 + 12345) & 2147483647
        rb = (state // 65536) % 9000 + 1

        a = ra
        for i in range(1, da):
            a = a * 10 % 1000000000000000 + (i % 10)
        b = rb
        for j in range(1, db):
            b = b * 10 % 1000000000000000 + (j % 10)
        if a > b:
            a, b = b, a

        sink = (sink + count_in_range(str(a), str(b))) % 1000000007
    print(sink)


main()

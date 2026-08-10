"""Benchmark workload for LeetCode #247 — Strobogrammatic Number II (Python; scale lane)."""

PAIR_A = ["0", "1", "6", "8", "9"]
PAIR_B = ["0", "1", "9", "8", "6"]


def build(k, n):
    if k == 0:
        return [""]
    if k == 1:
        return ["0", "1", "8"]
    out = []
    for s in build(k - 2, n):
        for p in range(5):
            if k == n and PAIR_A[p] == "0":
                continue
            out.append(PAIR_A[p] + s + PAIR_B[p])
    return out


def is_strobogrammatic(s):
    b = s.encode()
    if not b:
        return True
    lo, hi = 0, len(b) - 1
    while lo <= hi:
        x, y = b[lo], b[hi]
        ok = (x == 48 and y == 48) or (x == 49 and y == 49) or (x == 56 and y == 56) \
            or (x == 54 and y == 57) or (x == 57 and y == 54)
        if not ok:
            return False
        lo += 1
        hi -= 1
    return True


def main():
    n = 16
    rounds = 12
    sink = 0
    for _ in range(rounds):
        for s in build(n, n):
            if is_strobogrammatic(s):
                for c in s.encode():
                    sink = (sink * 31 + c) % 1000000007
    print(sink)


main()

"""LeetCode 296 benchmark lane — Python mirror of blackpixels.kara.

SCALED DOWN to 120 queries against the compiled lanes' 1200. The row/column
probes are per-pixel Python loops over a 4096-wide frame, which is exactly the
shape CPython is worst at, so at full scale this lane would dominate the
suite's wall clock for no extra information. BENCHMARKS.md's rule is to scale
the Python lane rather than let that happen.

The sink therefore does NOT match the other four — it is over a different
number of queries, by construction, and is only comparable to itself.

Uses `bytearray` and plain index loops rather than numpy: the point is to
mirror the same algorithm the other four run, not to measure a vectorised
library that would be doing something structurally different.
"""

N = 4096
QUERIES = 120

img = bytearray(N * N)
W = H = N


def row_has_black(r):
    base = r * W
    for c in range(W):
        if img[base + c] == 1:
            return True
    return False


def col_has_black(c):
    for r in range(H):
        if img[r * W + c] == 1:
            return True
    return False


def _bisect(lo, hi, pred):
    while lo < hi:
        m = lo + (hi - lo) // 2
        if pred(m):
            hi = m
        else:
            lo = m + 1
    return lo


def min_area(x, y):
    top = _bisect(0, x + 1, row_has_black)
    bottom = _bisect(x + 1, H, lambda r: not row_has_black(r))
    left = _bisect(0, y + 1, col_has_black)
    right = _bisect(y + 1, W, lambda c: not col_has_black(c))
    return (bottom - top) * (right - left)


def main():
    r0 = c0 = N // 2
    for r in range(40):
        for c in range(40):
            img[(r0 + r) * N + (c0 + c)] = 1
    for k in range(25):
        img[(r0 + 40 + k) * N + (c0 + 20)] = 1

    checksum = 0
    for q in range(QUERIES):
        sx = r0 + q % 40
        sy = c0 + (q * 7) % 40
        checksum = (checksum * 31 + min_area(sx, sy)) % 1000000007
    print(f"queries {QUERIES} checksum {checksum}")


if __name__ == "__main__":
    main()

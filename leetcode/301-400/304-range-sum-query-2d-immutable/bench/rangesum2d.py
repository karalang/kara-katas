# Benchmark mirror — LeetCode 304, Range Sum Query 2D (Immutable).
# Same algorithm, same flat prefix layout, same LCG, same masked sink as
# rangesum2d.kara. See ../README.md § Benchmarks.
#
# Note on the sink: `& 0x3FFFFFFF` is used rather than a modulo precisely
# because Python's `%` FLOORS while C/Rust/Go/kara truncate toward zero, so a
# modulo sink over a signed running total prints a different number here than
# in every other mirror (measured on #303: the two differed by exactly one
# modulus). Masking is two's-complement in all five languages.

import sys


def main():
    n = 256
    stride = n + 1
    queries = 100000
    passes = 1800
    state = 20304

    m = [0] * (n * n)
    for i in range(n * n):
        state = (state * 1103515245 + 12345) % 2147483648
        m[i] = state % 21 - 10

    pre = [0] * ((n + 1) * stride)
    for r in range(n):
        base, above = (r + 1) * stride, r * stride
        for c in range(n):
            pre[base + c + 1] = (pre[above + c + 1] + pre[base + c]
                                 - pre[above + c] + m[r * n + c])

    qr1 = [0] * queries
    qc1 = [0] * queries
    qr2 = [0] * queries
    qc2 = [0] * queries
    for q in range(queries):
        state = (state * 1103515245 + 12345) % 2147483648
        a = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        b = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        c = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        d = state % n
        qr1[q], qr2[q] = (a, b) if a <= b else (b, a)
        qc1[q], qc2[q] = (c, d) if c <= d else (d, c)

    checksum = 0
    for _ in range(passes):
        for k in range(queries):
            r1 = qr1[k]
            c1 = qc1[k]
            r2 = qr2[k]
            c2 = qc2[k]
            v = (pre[(r2 + 1) * stride + (c2 + 1)]
                 - pre[r1 * stride + (c2 + 1)]
                 - pre[(r2 + 1) * stride + c1]
                 + pre[r1 * stride + c1])
            checksum = (checksum + v) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()

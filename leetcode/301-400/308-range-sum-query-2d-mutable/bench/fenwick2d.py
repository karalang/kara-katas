# Benchmark mirror — LeetCode 308, Range Sum Query 2D (Mutable).
# Same 2D Fenwick tree, same LCG-generated operation script, same masked sink
# as fenwick2d.kara. See ../README.md § Benchmarks.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero, so a modulo sink over a signed running
# total prints a different number here than in every other mirror (measured on
# #303). Masking is two's-complement in all five languages.


def main():
    n = 256
    stride = n + 1
    ops = 100000
    passes = 54

    tree = [0] * ((n + 1) * stride)
    data = [0] * (n * n)
    kind = [0] * ops
    o1 = [0] * ops
    o2 = [0] * ops
    o3 = [0] * ops
    o4 = [0] * ops

    state = 20308
    for k in range(ops):
        state = (state * 1103515245 + 12345) % 2147483648
        t = state % 2
        state = (state * 1103515245 + 12345) % 2147483648
        a = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        b = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        c = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        d = state % n
        kind[k] = t
        if t == 0:
            o1[k], o2[k], o3[k], o4[k] = a, b, c % 2001 - 1000, 0
        else:
            o1[k], o3[k] = (a, c) if a <= c else (c, a)
            o2[k], o4[k] = (b, d) if b <= d else (d, b)

    checksum = 0
    for _ in range(passes):
        for k in range(ops):
            if kind[k] == 0:
                r, c = o1[k], o2[k]
                delta = o3[k] - data[r * n + c]
                data[r * n + c] = o3[k]
                x = r + 1
                while x <= n:
                    y = c + 1
                    while y <= n:
                        tree[x * stride + y] += delta
                        y += y & -y
                    x += x & -x
            else:
                r1, c1, r2, c2 = o1[k], o2[k], o3[k] + 1, o4[k] + 1
                total = 0
                for qi in range(4):
                    px, py, sign = r2, c2, 1
                    if qi == 1:
                        px, sign = r1, -1
                    if qi == 2:
                        py, sign = c1, -1
                    if qi == 3:
                        px, py = r1, c1
                    sub = 0
                    x = px
                    while x > 0:
                        y = py
                        while y > 0:
                            sub += tree[x * stride + y]
                            y -= y & -y
                        x -= x & -x
                    total += sign * sub
                checksum = (checksum + total) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()

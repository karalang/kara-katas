# Benchmark mirror — LeetCode 307, Range Sum Query (Mutable).
# Same Fenwick tree, same LCG-generated operation script, same masked sink as
# fenwick.kara. See ../README.md § Benchmarks.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero, so a modulo sink over a signed running
# total prints a different number here than in every other mirror (measured on
# #303). Masking is two's-complement in all five languages.


def main():
    n = 65536
    ops = 200000
    passes = 110

    tree = [0] * (n + 1)
    data = [0] * n
    kind = [0] * ops
    opa = [0] * ops
    opb = [0] * ops

    state = 20307
    for k in range(ops):
        state = (state * 1103515245 + 12345) % 2147483648
        t = state % 2
        state = (state * 1103515245 + 12345) % 2147483648
        x = state % n
        state = (state * 1103515245 + 12345) % 2147483648
        y = state % n
        kind[k] = t
        if t == 0:
            opa[k], opb[k] = x, y % 2001 - 1000
        elif x <= y:
            opa[k], opb[k] = x, y
        else:
            opa[k], opb[k] = y, x

    checksum = 0
    for _ in range(passes):
        for k in range(ops):
            if kind[k] == 0:
                i = opa[k]
                delta = opb[k] - data[i]
                data[i] = opb[k]
                x = i + 1
                while x <= n:
                    tree[x] += delta
                    x += x & -x
            else:
                total = 0
                hi = opb[k] + 1
                while hi > 0:
                    total += tree[hi]
                    hi -= hi & -hi
                lo = opa[k]
                while lo > 0:
                    total -= tree[lo]
                    lo -= lo & -lo
                checksum = (checksum + total) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()

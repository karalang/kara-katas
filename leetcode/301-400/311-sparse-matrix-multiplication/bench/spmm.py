# Benchmark mirror — LeetCode 311, Sparse Matrix Multiplication.
# Same flat row-major layout, same LCG, same zero-skipping multiply, same
# per-pass perturbation and masked sink as spmm.kara. See ../README.md.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero (measured on #303).


def main():
    n = 320
    passes = 620
    cells = n * n
    a = [0] * cells
    b = [0] * cells
    c = [0] * cells
    state = 20311
    for i in range(cells):
        state = (state * 1103515245 + 12345) % 2147483648
        if state % 100 < 4:
            state = (state * 1103515245 + 12345) % 2147483648
            a[i] = state % 9 - 4
        else:
            a[i] = 0
        state = (state * 1103515245 + 12345) % 2147483648
        if state % 100 < 4:
            state = (state * 1103515245 + 12345) % 2147483648
            b[i] = state % 9 - 4
        else:
            b[i] = 0

    checksum = 0
    for p in range(passes):
        slot = (p * 7919) % cells
        a[slot] = a[slot] + (checksum & 1)
        for i in range(cells):
            c[i] = 0
        for r in range(n):
            arow = r * n
            for k in range(n):
                av = a[arow + k]
                if av != 0:
                    brow = k * n
                    for j in range(n):
                        c[arow + j] += av * b[brow + j]
        acc = 0
        for t in range(cells):
            acc = (acc + c[t]) & 0x3FFFFFFF
        checksum = (checksum + acc) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()

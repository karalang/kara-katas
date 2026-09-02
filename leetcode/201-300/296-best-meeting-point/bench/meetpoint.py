"""Benchmark mirror of meetpoint.kara - LeetCode #296, separable medians.

Same two scans (row-major then column-major), same reused scratch, same sink.
Written as explicit index loops rather than comprehensions so it times the same
algorithm the other four mirrors run, not Python's fastest way to say it.
"""

NCASES = 400
DIM = 128
PASSES = 30
CELLS = DIM * DIM
MOD = 1000000007


def main() -> None:
    corpus = bytearray(NCASES * CELLS)
    state = 24601
    for n in range(NCASES * CELLS):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        if (state // 65536) % 100 < 10:
            corpus[n] = 1

    rows = [0] * CELLS
    cols = [0] * CELLS
    checksum = 0

    for _ in range(PASSES):
        for ci in range(NCASES):
            base = ci * CELLS

            k = 0
            for r in range(DIM):
                row_base = base + r * DIM
                for c in range(DIM):
                    if corpus[row_base + c] == 1:
                        rows[k] = r
                        k += 1

            k2 = 0
            for c in range(DIM):
                for r in range(DIM):
                    if corpus[base + r * DIM + c] == 1:
                        cols[k2] = c
                        k2 += 1

            total = 0
            if k > 0:
                mr = rows[k // 2]
                mc = cols[k // 2]
                for i in range(k):
                    dr = rows[i] - mr
                    total += -dr if dr < 0 else dr
                    dc = cols[i] - mc
                    total += -dc if dc < 0 else dc

            checksum = (checksum + total) % MOD

    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()

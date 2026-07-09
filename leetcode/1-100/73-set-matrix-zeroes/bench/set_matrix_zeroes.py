"""Benchmark workload — Set Matrix Zeroes (LeetCode #73).

Python mirror of bench/set_matrix_zeroes.kara. Same O(1)-space first-row/col
marker algorithm, same growing list-of-lists build (append, not a preallocated
grid), same three punched zeros, K=100_000 iters over a 20×20 matrix. Emits the
same single polynomial-hash sink so it cross-checks the compiled mirrors.
"""

from __future__ import annotations


def set_zeroes(m: list[list[int]]) -> None:
    rows = len(m)
    if rows == 0:
        return
    cols = len(m[0])

    first_row_zero = any(m[0][j] == 0 for j in range(cols))
    first_col_zero = any(m[i][0] == 0 for i in range(rows))

    for i in range(1, rows):
        for j in range(1, cols):
            if m[i][j] == 0:
                m[i][0] = 0
                m[0][j] = 0

    for i in range(1, rows):
        for j in range(1, cols):
            if m[i][0] == 0 or m[0][j] == 0:
                m[i][j] = 0

    if first_row_zero:
        for j in range(cols):
            m[0][j] = 0
    if first_col_zero:
        for i in range(rows):
            m[i][0] = 0


def main() -> None:
    total = 100000
    modulus = 1000000007
    rows = 20
    cols = 20

    acc = 0
    for k in range(total):
        m: list[list[int]] = []
        for i in range(rows):
            row: list[int] = []
            for j in range(cols):
                row.append(1 + (i * 31 + j * 17 + k) % 9)
            m.append(row)
        m[k % rows][k % cols] = 0
        m[(k * 7) % rows][(k * 13) % cols] = 0
        m[(k * 3) % rows][(k * 11) % cols] = 0

        set_zeroes(m)

        for i in range(rows):
            for j in range(cols):
                acc = (acc * 131 + m[i][j]) % modulus
    print(acc)


if __name__ == "__main__":
    main()

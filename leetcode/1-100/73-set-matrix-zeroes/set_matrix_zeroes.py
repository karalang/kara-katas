"""LeetCode #73: Set Matrix Zeroes — O(1) extra space, first row/col as markers.

Mirror of set_matrix_zeroes.kara. If a cell is 0, its whole row and column become
0, in place. The first row and first column double as the marker storage; two
bools remember whether row 0 / col 0 were themselves originally zero, applied
last. Same ten cases and the same output shape (the mutated grid per case, a
`---` separator, then a `sums:` fold of a per-grid polynomial hash) so the files
diff line-for-line. (The O(m+n) markers variant lives only in Kāra; this mirror
tracks the O(1) star.)
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


def print_grid(m: list[list[int]]) -> None:
    for row in m:
        print("[" + ", ".join(str(x) for x in row) + "]")


def hash_grid(m: list[list[int]]) -> int:
    acc = 0
    for row in m:
        for x in row:
            acc = (acc * 131 + x) % 1000000007
    return acc


def report(grid: list[list[int]], acc: list[str]) -> None:
    set_zeroes(grid)
    print_grid(grid)
    print("---")
    acc.append(str(hash_grid(grid)))


def main() -> None:
    acc: list[str] = []
    report([[1, 1, 1], [1, 0, 1], [1, 1, 1]], acc)
    report([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], acc)
    report([[0]], acc)
    report([[7]], acc)
    report([[1, 2], [3, 4]], acc)
    report([[0, 0], [0, 0]], acc)
    report([[5, 0, 9, 3]], acc)
    report([[5], [0], [9], [3]], acc)
    report([[1, 2, 3], [0, 4, 5], [6, 7, 8]], acc)
    report([[1, 0, 3], [4, 5, 6], [7, 8, 9]], acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()

"""LeetCode #48: Rotate Image — known-correct reference oracle.

Given an `n x n` matrix, rotate it 90 degrees CLOCKWISE, IN PLACE (the follow-up forbids
allocating a second matrix). The single fact every solver encodes is the clockwise index map

    new[i][j] = old[n-1-j][i]      (equivalently: old[i][j] lands at new[j][n-1-i])

Four canonical factorings, all producing the IDENTICAL rotated matrix for every case
(cross-checked below), each mirroring one Kāra pedagogical file:

  - Style 1 (layer-by-layer four-way cyclic swap, ★) — mirror of rotate_image.kara
  - Style 2 (transpose, then reverse each row)        — mirror of rotate_image_transpose.kara
  - Style 3 (reverse the row order, then transpose)   — mirror of rotate_image_flip.kara
  - Style 4 (out-of-place index map into a fresh grid) — mirror of rotate_image_fresh.kara

Styles 1–3 mutate a copy in place (O(1) extra space); Style 4 is the explicit-mapping contrast
that the in-place follow-up rules out, kept because it states the index arithmetic outright. The
harness echoes the input matrix, a `->` line, then the rotated matrix, then `---`, so each Kāra
mirror's stdout is line-for-line diffable under both `karac run` and `karac build`.

LeetCode bounds: 1 ≤ n ≤ 20, -1000 ≤ matrix[i][j] ≤ 1000 — every value fits in i64.
"""

from __future__ import annotations


# --- Style 1: layer-by-layer four-way cyclic swap (mirrors rotate_image.kara, ★) ---
#
# Walk concentric rings (layers). For each ring, rotate its four sides one quarter-turn by
# cycling four cells at a time: the top cell moves to the right, right to bottom, bottom to
# left, left to top. The four positions in one cycle are
#   top    = (i,       j)
#   right  = (j,       n-1-i)
#   bottom = (n-1-i,   n-1-j)
#   left   = (n-1-j,   i)
# and the clockwise move is `top, right, bottom, left = left, top, right, bottom` — a
# single four-way parallel assignment, no temporary. O(1) extra space.

def rotate_cycle(m: list[list[int]]) -> list[list[int]]:
    a = [row[:] for row in m]
    n = len(a)
    for i in range(n // 2):
        for j in range(i, n - 1 - i):
            (a[i][j], a[j][n - 1 - i], a[n - 1 - i][n - 1 - j], a[n - 1 - j][i]) = (
                a[n - 1 - j][i], a[i][j], a[j][n - 1 - i], a[n - 1 - i][n - 1 - j])
    return a


# --- Style 2: transpose, then reverse each row (mirrors rotate_image_transpose.kara) ---
#
# A 90°-clockwise rotation factors into two in-place passes: transpose across the main
# diagonal (swap a[i][j] with a[j][i] for j > i), then reverse every row left-to-right.

def rotate_transpose(m: list[list[int]]) -> list[list[int]]:
    a = [row[:] for row in m]
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]
    for i in range(n):
        a[i].reverse()
    return a


# --- Style 3: reverse the row order, then transpose (mirrors rotate_image_flip.kara) ---
#
# The dual identity of Style 2: flip the matrix top-to-bottom (reverse the list of rows),
# then transpose. Same 90° clockwise result, with the cheap pass (whole-row reversal of the
# outer list) done first.

def rotate_flip(m: list[list[int]]) -> list[list[int]]:
    a = [row[:] for row in m]
    n = len(a)
    a.reverse()
    for i in range(n):
        for j in range(i + 1, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]
    return a


# --- Style 4: out-of-place index map into a fresh grid (mirrors rotate_image_fresh.kara) ---
#
# The straight-line statement of the rotation: allocate a fresh n×n grid and scatter each
# source cell to its rotated home, `dst[j][n-1-i] = src[i][j]`. Violates the in-place
# follow-up, but names the index arithmetic the three in-place forms encode implicitly.

def rotate_fresh(m: list[list[int]]) -> list[list[int]]:
    n = len(m)
    dst = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dst[j][n - 1 - i] = m[i][j]
    return dst


def show_row(row: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in row) + "]"


def report(m: list[list[int]]) -> None:
    a = rotate_cycle(m)
    b = rotate_transpose(m)
    c = rotate_flip(m)
    d = rotate_fresh(m)
    assert a == b == c == d, (m, a, b, c, d)
    for row in m:
        print(show_row(row))
    print("->")
    for row in a:
        print(show_row(row))
    print("---")


def main() -> None:
    # LeetCode example 1 — 3×3.
    report([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # LeetCode example 2 — 4×4.
    report([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]])
    # The 1×1 degenerate case — rotation is identity.
    report([[1]])
    # The smallest non-trivial ring — 2×2 (no center cell).
    report([[1, 2], [3, 4]])
    # A 5×5 with an odd center and negative values.
    report([[-1, 2, -3, 4, -5],
            [6, -7, 8, -9, 10],
            [-11, 12, -13, 14, -15],
            [16, -17, 18, -19, 20],
            [-21, 22, -23, 24, -25]])


if __name__ == "__main__":
    main()

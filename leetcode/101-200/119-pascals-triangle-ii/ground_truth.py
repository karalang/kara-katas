#!/usr/bin/env python3
"""Ground-truth check for LeetCode #119 — three independent ways must agree.

The rowIndex-th row of Pascal's triangle, verified three ways that must produce the identical row:

  1. In-place rolling — one row, updated right-to-left `row[j] += row[j-1]` (`get_row.kara`, the ★).
  2. Binomial multiplicative — `C(n, j) = C(n, j-1) * (n - j + 1) / j` (`get_row_binomial.kara`).
  3. Definition — `C(n, j)` via Python's exact-integer `math.comb`.

Checked for every row_index in 0..80 (well past the LeetCode `≤ 33` constraint — the extra range
stress-tests the multiplicative form's exactness as coefficients grow, though only the arbitrary-
precision Python check runs that high; the compiled i64 solvers stay within their overflow-safe
range). Zero disagreements is the pass — the oracle the Kara solvers are trusted against."""

from math import comb


def get_row_inplace(n):
    row = [1] * (n + 1)
    for i in range(2, n + 1):
        for k in range(i - 1, 0, -1):
            row[k] = row[k] + row[k - 1]
    return row


def get_row_binomial(n):
    row = []
    c = 1
    for j in range(n + 1):
        row.append(c)
        c = c * (n - j) // (j + 1)
    return row


def get_row_def(n):
    return [comb(n, j) for j in range(n + 1)]


def main():
    fails = 0
    for n in range(0, 81):
        a = get_row_inplace(n)
        b = get_row_binomial(n)
        d = get_row_def(n)
        if not (a == b == d):
            fails += 1
            if fails <= 5:
                print(f"FAIL at row_index={n}")
    if fails == 0:
        print("ground truth OK: in-place == binomial == C(n,j) definition (row_index 0..80, 0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

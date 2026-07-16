#!/usr/bin/env python3
"""Ground-truth check for LeetCode #118 — three independent ways must agree.

Pascal's triangle can be generated three ways that must produce the identical table:

  1. Additive — each row from the previous (`row[j] = prev[j-1] + prev[j]`, edges 1) (`generate.kara`).
  2. Binomial multiplicative — `C(i, j) = C(i, j-1) * (i - j + 1) / j` per row, no previous-row
     dependence (`generate_binomial.kara`).
  3. Definition — `C(i, j) = i! / (j! (i-j)!)` via Python's exact-integer `math.comb`.

We check all three produce the identical triangle for every `num_rows` in 0…60 (well past the
LeetCode `≤ 30` constraint — the extra range stress-tests the multiplicative form's exactness where
the coefficients grow large but still fit i64). Zero disagreements is the pass — the oracle the Kara
solvers are trusted against."""

from math import comb


def gen_additive(num_rows):
    tri = []
    for i in range(num_rows):
        row = []
        for j in range(i + 1):
            if j == 0 or j == i:
                row.append(1)
            else:
                row.append(tri[i - 1][j - 1] + tri[i - 1][j])
        tri.append(row)
    return tri


def gen_binomial(num_rows):
    tri = []
    for i in range(num_rows):
        row = []
        c = 1
        for j in range(i + 1):
            row.append(c)
            c = c * (i - j) // (j + 1)
        tri.append(row)
    return tri


def gen_definition(num_rows):
    return [[comb(i, j) for j in range(i + 1)] for i in range(num_rows)]


def main():
    fails = 0
    for n in range(0, 61):
        a = gen_additive(n)
        b = gen_binomial(n)
        d = gen_definition(n)
        if not (a == b == d):
            fails += 1
            if fails <= 5:
                print(f"FAIL at num_rows={n}")
    if fails == 0:
        print("ground truth OK: additive == binomial == C(i,j) definition (num_rows 0..60, 0 disagreements)")
    else:
        print(f"GROUND TRUTH FAILED: {fails} disagreements")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

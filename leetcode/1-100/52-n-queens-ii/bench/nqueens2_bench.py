"""Bench mirror of nqueens2_bench.kara — return-value counting backtracker,
weighted-checksum int sink, swept over n = 9..13. CPython.
See ../README.md § Benchmarks.

CPython is ~2 orders of magnitude slower on this recursive kernel, so it is
excluded from the headline table by default (KARA_BENCH_INCLUDE_PY=1 to include).
"""

import sys


def search(n, row, cols, diag1, diag2, partial):
    if row == n:
        return 1 + partial
    acc = 0
    for c in range(n):
        bit_c = 1 << c
        bit_d1 = 1 << (row + c)
        bit_d2 = 1 << (row - c + (n - 1))
        if (cols & bit_c) == 0 and (diag1 & bit_d1) == 0 and (diag2 & bit_d2) == 0:
            acc += search(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2,
                          partial + c * (row + 1))
    return acc


def main() -> None:
    n_lo, n_hi = 9, 13
    total = 0
    for n in range(n_lo, n_hi + 1):
        total += search(n, 0, 0, 0, 0, 0)
    print(total)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()

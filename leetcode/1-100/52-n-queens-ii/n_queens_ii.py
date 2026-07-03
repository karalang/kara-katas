"""LeetCode #52: N-Queens II — algorithmic mirror of bitmask_count.kara (the ★ solver).

Row-by-row backtracking with three integer occupancy bitmasks (columns, ↘ diagonals
keyed by row+col, ↙ diagonals keyed by row-col+(n-1)), threaded by value and summed
by return value — exactly the ★ .kara kernel. Prints `n -> count` for n = 1..11 plus a
`counts:` summary line, so this oracle diffs byte-for-byte against `karac run` /
`karac build` output for all three .kara solvers (which all reach the identical counts).
"""

from __future__ import annotations


def count(n: int, row: int, cols: int, diag1: int, diag2: int) -> int:
    if row == n:
        return 1
    total = 0
    for c in range(n):
        bit_c = 1 << c
        bit_d1 = 1 << (row + c)
        bit_d2 = 1 << (row - c + (n - 1))
        if (cols & bit_c) == 0 and (diag1 & bit_d1) == 0 and (diag2 & bit_d2) == 0:
            total += count(n, row + 1, cols | bit_c, diag1 | bit_d1, diag2 | bit_d2)
    return total


def solve(n: int) -> int:
    return count(n, 0, 0, 0, 0)


def main() -> None:
    parts = ["counts:"]
    for n in range(1, 12):
        c = solve(n)
        print(f"n={n} -> {c}")
        parts.append(str(c))
    print(" ".join(parts))


if __name__ == "__main__":
    main()

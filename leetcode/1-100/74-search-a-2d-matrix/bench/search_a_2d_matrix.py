"""Benchmark workload — Search a 2D Matrix (LeetCode #74).

Python mirror of bench/search_a_2d_matrix.kara. Same flattened binary search over
a 100x100 list-of-lists matrix built once, same target schedule. Runs K=1,000,000
queries — 1/10 of the compiled mirrors' K=10,000,000 — because a pure-Python
binary-search loop at full scale is ~70 s/run; this row is timed separately and
its sink is NOT cross-checked against the compiled sink (different K). The kata's
correctness is verified by the top-level search_a_2d_matrix.py oracle instead.
"""

from __future__ import annotations


def search_matrix(m: list[list[int]], target: int) -> bool:
    rows = len(m)
    if rows == 0:
        return False
    cols = len(m[0])
    if cols == 0:
        return False
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        v = m[mid // cols][mid % cols]
        if v == target:
            return True
        elif v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def main() -> None:
    rows, cols = 100, 100
    total = 1_000_000  # 1/10 of the compiled mirrors' K; timed-only, not cross-checked
    modulus = 1_000_000_007
    rng = 2 * rows * cols

    m = [[(i * cols + j) * 2 for j in range(cols)] for i in range(rows)]

    acc = 0
    for k in range(total):
        target = k % rng
        bit = 1 if search_matrix(m, target) else 0
        acc = (acc * 131 + bit) % modulus
    print(acc)


if __name__ == "__main__":
    main()

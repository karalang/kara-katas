"""Benchmark workload — binary-search-partition O(log min(m, n)) Median of
Two Sorted Arrays.

Algorithmic mirror of bench/binary_search_partition.kara. See ../README.md
§ Benchmarks for the choice of M, N, R, K and the rotated-input shape.
"""

from __future__ import annotations

import sys


def middle_pair_off(a: list[int], a_off: int, a_len: int,
                    b: list[int], b_off: int, b_len: int) -> tuple[int, int]:
    if a_len > b_len:
        return middle_pair_off(b, b_off, b_len, a, a_off, a_len)
    half = (a_len + b_len + 1) // 2
    neg_inf = -(1 << 62)
    pos_inf = (1 << 62)
    lo, hi = 0, a_len
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        left_a  = a[a_off + i - 1] if i > 0     else neg_inf
        right_a = a[a_off + i]     if i < a_len else pos_inf
        left_b  = b[b_off + j - 1] if j > 0     else neg_inf
        right_b = b[b_off + j]     if j < b_len else pos_inf
        if left_a > right_b:
            hi = i - 1
        elif left_b > right_a:
            lo = i + 1
        else:
            lower = max(left_a, left_b)
            if (a_len + b_len) % 2 == 1:
                return (lower, lower)
            upper = min(right_a, right_b)
            return (lower, upper)
    raise AssertionError("unreachable")


def main() -> None:
    M = 1_000_000
    N = 1_000_000
    R = 1_000
    K = 10_000_000

    base_a = [2 * p for p in range(M + R)]
    base_b = [2 * p + 1 for p in range(N + R)]

    sum_result = 0
    for k in range(K):
        off = k % R
        lower, upper = middle_pair_off(base_a, off, M, base_b, off, N)
        sum_result += lower + upper
    print(sum_result)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    main()

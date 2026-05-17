"""LeetCode #4: Median of Two Sorted Arrays — binary-search partition.
O(log(min(m, n))) time, O(1) extra space.

Algorithmic mirror of binary_search_partition.kara. Output format matches
line-for-line so the two can be diffed directly.
"""

from __future__ import annotations

import sys


def middle_pair(a: list[int], b: list[int]) -> tuple[int, int]:
    # Returns (lower_median, upper_median) — the (T+1)/2-th and (T+2)/2-th
    # smallest elements of the merged sequence (1-indexed, T = len(a)+len(b)).
    # For odd T they are equal; for even T they are the two middle elements.
    # The median is their arithmetic mean.
    if len(a) > len(b):
        return middle_pair(b, a)
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    neg_inf = -(1 << 62)
    pos_inf = (1 << 62)
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        left_a  = a[i - 1] if i > 0 else neg_inf
        right_a = a[i]     if i < m else pos_inf
        left_b  = b[j - 1] if j > 0 else neg_inf
        right_b = b[j]     if j < n else pos_inf
        if left_a > right_b:
            hi = i - 1
        elif left_b > right_a:
            lo = i + 1
        else:
            lower = max(left_a, left_b)
            # For odd T, (T+2)//2 == (T+1)//2, so the upper median equals the
            # lower median — duplicate it so the printed pair always satisfies
            # median = (lower + upper) / 2. For even T, the upper median is the
            # smallest element of the right partition.
            if (m + n) % 2 == 1:
                return (lower, lower)
            upper = min(right_a, right_b)
            return (lower, upper)
    raise AssertionError("unreachable on valid sorted inputs")


def report(a: list[int], b: list[int]) -> None:
    lower, upper = middle_pair(a, b)
    print(lower)
    print(upper)


def main() -> None:
    # Two lines per case: lower median, then upper median. The median is
    # (lower + upper) / 2; for odd-total cases lower == upper. See
    # README § Output format for why we report the pair rather than the float.
    report([1, 3], [2])                            # T=3  → 2 2          (median 2.0)
    report([1, 2], [3, 4])                         # T=4  → 2 3          (median 2.5)
    report([], [1])                                # T=1  → 1 1          (median 1.0)
    report([2], [])                                # T=1  → 2 2          (median 2.0)
    report([1], [2])                               # T=2  → 1 2          (median 1.5)
    report([1, 2, 3, 4], [])                       # T=4  → 2 3          (median 2.5)
    report([1, 3, 8], [2, 4, 7, 9])                # T=7  → 4 4          (median 4.0)
    report([1, 1, 1], [1, 1])                      # T=5  → 1 1          (all equal)
    report([5, 6, 7, 8], [1, 2])                   # T=6  → 5 6          (median 5.5, triggers swap)
    report([-5, -3], [-2, 0, 1])                   # T=5  → -2 -2        (negatives)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)  # the swap recursion goes one level deep
    main()

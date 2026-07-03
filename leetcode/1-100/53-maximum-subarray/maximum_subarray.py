"""LeetCode #53: Maximum Subarray — algorithmic mirror of kadane.kara (the ★ solver).

Kadane's O(n) DP: sweep left to right holding `here` = the largest subarray sum that
ENDS at the current index (`max(x, here + x)`), and `best` = the largest such value seen
anywhere. Seeds both with nums[0], so an all-negative array correctly returns its single
largest element rather than 0 (the empty subarray is not allowed). Prints one answer per
test case plus a `sums:` summary line, so this oracle diffs byte-for-byte against
`karac run` / `karac build` output for all three .kara solvers (which all reach the
identical answers).
"""

from __future__ import annotations


def max_subarray(nums: list[int]) -> int:
    best = here = nums[0]
    for x in nums[1:]:
        here = max(x, here + x)
        best = max(best, here)
    return best


CASES: list[list[int]] = [
    [-2, 1, -3, 4, -1, 2, 1, -5, 4],
    [1],
    [5, 4, -1, 7, 8],
    [-1],
    [-2, -1],
    [-3, -2, -5, -1],
    [8, -19, 5, -4, 20],
    [1, 2, 3, 4, 5],
    [3, -2, 5, -1],
    [-5, -4, -3, -2, -1],
    [0],
    [-1, 0, -2],
]


def main() -> None:
    parts = ["sums:"]
    for nums in CASES:
        ans = max_subarray(nums)
        print(ans)
        parts.append(str(ans))
    print(" ".join(parts))


if __name__ == "__main__":
    main()

"""LeetCode #31: Next Permutation — known-correct reference oracle.

Algorithmic mirror of next_permutation.kara (the canonical four-move scan).
Output format matches line-for-line so the two can be diffed directly. The
binary-search variant (next_permutation_bsearch.kara) produces identical output.
"""

from __future__ import annotations


def next_permutation(nums: list[int], length: int) -> None:
    # 1. Pivot: rightmost i with nums[i] < nums[i + 1].
    i = length - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    # 3. Successor: rightmost j (in the descending suffix) with nums[j] > nums[i].
    if i >= 0:
        j = length - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    # 4. Reverse the suffix nums[i + 1 ..] (descending -> ascending); i = -1
    #    reverses the whole array — the wrap from greatest back to least.
    lo, hi = i + 1, length - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1


def fmt(nums: list[int], length: int) -> str:
    return "[" + ", ".join(str(nums[i]) for i in range(length)) + "]"


def report(nums: list[int]) -> None:
    before = fmt(nums, len(nums))
    next_permutation(nums, len(nums))
    print(f"{before} -> {fmt(nums, len(nums))}")


def main() -> None:
    report([1, 2, 3])              # [1, 2, 3] -> [1, 3, 2]
    report([3, 2, 1])             # [3, 2, 1] -> [1, 2, 3]
    report([1, 1, 5])             # [1, 1, 5] -> [1, 5, 1]
    report([1, 5, 4, 3, 2])      # [1, 5, 4, 3, 2] -> [2, 1, 3, 4, 5]
    report([1, 3, 2, 2, 2, 1])  # [1, 3, 2, 2, 2, 1] -> [2, 1, 1, 2, 2, 3]
    report([1, 2])               # [1, 2] -> [2, 1]
    report([2, 1])               # [2, 1] -> [1, 2]
    report([7])                  # [7] -> [7]
    report([2, 2, 2, 2])         # [2, 2, 2, 2] -> [2, 2, 2, 2]
    report([1, 2, 3, 6, 5, 4])  # [1, 2, 3, 6, 5, 4] -> [1, 2, 4, 3, 5, 6]
    report([-1, 0, -2, 3])      # [-1, 0, -2, 3] -> [-1, 0, 3, -2]


if __name__ == "__main__":
    main()

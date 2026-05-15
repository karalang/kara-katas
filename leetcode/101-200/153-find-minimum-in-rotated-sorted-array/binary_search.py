"""LeetCode #153: Find Minimum in Rotated Sorted Array — binary search O(log n).

Algorithmic mirror of binary_search.kara. Output format matches line-for-line
so the two can be diffed directly.
"""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    # Invariant: the minimum is in [lo, hi]. Compare nums[mid] against
    # nums[hi]: if mid is greater, the drop is strictly right of mid; else
    # mid and everything right of it is sorted, so hi := mid.
    lo = 0
    hi = len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


def report(nums: list[int]) -> None:
    print(find_min(nums))


def main() -> None:
    report([3, 4, 5, 1, 2])         # expect: 1
    report([4, 5, 6, 7, 0, 1, 2])   # expect: 0
    report([11, 13, 15, 17])        # expect: 11
    report([5])                     # expect: 5
    report([2, 1])                  # expect: 1


if __name__ == "__main__":
    main()

"""LeetCode #153: Find Minimum in Rotated Sorted Array — linear scan O(n).

Algorithmic mirror of linear_scan.kara. Output format matches line-for-line
so the two can be diffed directly.
"""

from __future__ import annotations


def find_min(nums: list[int]) -> int:
    m = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        if x < m:
            m = x
    return m


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

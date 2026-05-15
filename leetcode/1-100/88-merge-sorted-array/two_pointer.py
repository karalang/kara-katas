"""LeetCode #88: Merge Sorted Array — two pointers from the back, in-place.

Algorithmic mirror of two_pointer.kara. Output format matches line-for-line so
the two can be diffed directly.
"""

from __future__ import annotations


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    # Write from the back: the write head k = m + n - 1 is always at or past
    # both read heads i and j, so every cell is written before it would be read.
    i = m - 1
    j = n - 1
    k = m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1


def report(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    merge(nums1, m, nums2, n)
    for x in nums1[: m + n]:
        print(x)


def main() -> None:
    report([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3)   # expect: 1 2 2 3 5 6
    report([1], 1, [], 0)                          # expect: 1
    report([0], 0, [1], 1)                         # expect: 1
    report([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3)   # expect: 1 2 3 4 5 6
    report([1, 2, 3, 0, 0, 0], 3, [4, 5, 6], 3)   # expect: 1 2 3 4 5 6


if __name__ == "__main__":
    main()

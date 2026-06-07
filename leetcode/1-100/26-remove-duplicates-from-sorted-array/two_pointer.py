"""LeetCode #26: Remove Duplicates from Sorted Array — two pointers, in-place.

Algorithmic mirror of two_pointer.kara. Output format matches line-for-line so
the two can be diffed directly.
"""

from __future__ import annotations


def remove_duplicates(nums: list[int], length: int) -> int:
    # nums[0..k] is the deduplicated prefix of everything read so far; sorted
    # input means "new value" is one compare against nums[k - 1].
    if length == 0:
        return 0
    k = 1
    for i in range(1, length):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return k


def report(nums: list[int], length: int) -> None:
    k = remove_duplicates(nums, length)
    print(f"k = {k}")
    for x in nums[:k]:
        print(x)


def main() -> None:
    report([1, 1, 2], 3)                            # expect: k = 2, then 1 2
    report([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 10)      # expect: k = 5, then 0 1 2 3 4
    report([7], 1)                                  # expect: k = 1, then 7
    report([5, 5, 5, 5], 4)                         # expect: k = 1, then 5
    report([1, 2, 3], 3)                            # expect: k = 3, then 1 2 3
    report([-3, -3, -1, 0, 0], 5)                   # expect: k = 3, then -3 -1 0
    report([], 0)                                   # expect: k = 0


if __name__ == "__main__":
    main()

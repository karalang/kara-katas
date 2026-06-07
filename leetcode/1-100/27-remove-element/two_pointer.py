"""LeetCode #27: Remove Element — two pointers, in-place.

Algorithmic mirror of two_pointer.kara. Output format matches line-for-line so
the two can be diffed directly.
"""

from __future__ import annotations


def remove_element(nums: list[int], length: int, val: int) -> int:
    # nums[0..k] is the compaction of every kept element read so far; the
    # keep test is a compare against the scalar val (no sorted-input or
    # nums[k - 1] lookback, unlike kata #26).
    k = 0
    for i in range(length):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k


def report(nums: list[int], length: int, val: int) -> None:
    k = remove_element(nums, length, val)
    print(f"k = {k}")
    for x in nums[:k]:
        print(x)


def main() -> None:
    report([3, 2, 2, 3], 4, 3)                  # expect: k = 2, then 2 2
    report([0, 1, 2, 2, 3, 0, 4, 2], 8, 2)      # expect: k = 5, then 0 1 3 0 4
    report([4, 4, 4], 3, 4)                      # expect: k = 0
    report([1, 2, 3], 3, 5)                      # expect: k = 3, then 1 2 3
    report([], 0, 0)                            # expect: k = 0
    report([1], 1, 1)                           # expect: k = 0
    report([1], 1, 2)                           # expect: k = 1, then 1
    report([-1, 0, -1, 2, -1], 5, -1)           # expect: k = 2, then 0 2


if __name__ == "__main__":
    main()

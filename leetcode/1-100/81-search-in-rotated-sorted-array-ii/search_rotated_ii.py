"""LeetCode #81: Search in Rotated Sorted Array II — modified binary search w/ dups.

Mirror of search_rotated_ii.kara. Kata #33's rotated binary search plus the one new
branch that makes it duplicate-safe: when nums[lo] == nums[mid] == nums[hi] the
"which half is sorted?" test is uninformative, so shrink both ends by one and retry
(the step that makes the worst case O(n)). Returns a boolean. Same nineteen queries
and output shape (an `[array] target=t -> true/false` line per query, then a `sink:`
fold of target + outcome) so the files diff line-for-line.
"""

from __future__ import annotations


def search(nums: list[int], length: int, target: int) -> bool:
    lo = 0
    hi = length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] and nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False


def fmt(nums: list[int], length: int) -> str:
    return "[" + ", ".join(str(nums[i]) for i in range(length)) + "]"


def report(nums: list[int], length: int, target: int, acc: list[int]) -> None:
    found = search(nums, length, target)
    print(f"{fmt(nums, length)} target={target} -> {'true' if found else 'false'}")
    bit = 1 if found else 0
    acc[0] = (acc[0] * 131 + (target + 1000) * 2 + bit) % 1000000007


def main() -> None:
    acc = [0]
    report([2, 5, 6, 0, 0, 1, 2], 7, 0, acc)
    report([2, 5, 6, 0, 0, 1, 2], 7, 3, acc)
    report([1, 1, 1, 2, 1, 1, 1], 7, 2, acc)
    report([1, 1, 1, 2, 1, 1, 1], 7, 3, acc)
    report([5, 5, 5, 5, 5, 5], 6, 5, acc)
    report([5, 5, 5, 5, 5, 5], 6, 7, acc)
    report([4, 5, 6, 6, 7, 0, 1, 2, 4], 9, 6, acc)
    report([4, 5, 6, 6, 7, 0, 1, 2, 4], 9, 0, acc)
    report([4, 5, 6, 6, 7, 0, 1, 2, 4], 9, 3, acc)
    report([1, 1, 1, 1, 2, 3, 1, 1], 8, 3, acc)
    report([1, 1, 1, 1, 2, 3, 1, 1], 8, 0, acc)
    report([1, 2, 2, 3, 4], 5, 2, acc)
    report([1, 2, 2, 3, 4], 5, 5, acc)
    report([1, 3], 2, 3, acc)
    report([1, 3], 2, 2, acc)
    report([1], 1, 1, acc)
    report([1], 1, 0, acc)
    report([], 0, 5, acc)
    report([-1, -1, 3, 3, -2, -1], 6, -2, acc)
    report([-1, -1, 3, 3, -2, -1], 6, 0, acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()

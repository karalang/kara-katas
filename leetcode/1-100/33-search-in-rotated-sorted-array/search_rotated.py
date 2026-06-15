"""LeetCode #33: Search in Rotated Sorted Array — known-correct reference oracle.

Algorithmic mirror of search_rotated.kara (the one-pass modified binary search).
Output format matches line-for-line so the two can be diffed directly. The pivot
and remap variants produce identical output; this oracle additionally cross-checks
all three algorithms agree on every case (and against Python's own `index`).
"""

from __future__ import annotations


def search_one_pass(nums: list[int], length: int, target: int) -> int:
    lo, hi = 0, length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def find_pivot(nums: list[int], length: int) -> int:
    lo, hi = 0, length - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bsearch(nums: list[int], lo: int, hi: int, target: int) -> int:
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_pivot(nums: list[int], length: int, target: int) -> int:
    if length == 0:
        return -1
    pivot = find_pivot(nums, length)
    if pivot == 0:
        return bsearch(nums, 0, length - 1, target)
    if nums[0] <= target <= nums[pivot - 1]:
        return bsearch(nums, 0, pivot - 1, target)
    return bsearch(nums, pivot, length - 1, target)


def search_remap(nums: list[int], length: int, target: int) -> int:
    if length == 0:
        return -1
    rot = find_pivot(nums, length)
    lo, hi = 0, length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        real = (mid + rot) % length
        v = nums[real]
        if v == target:
            return real
        elif v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


CASES = [
    ([4, 5, 6, 7, 0, 1, 2], 0),
    ([4, 5, 6, 7, 0, 1, 2], 3),
    ([1], 0),
    ([1], 1),
    ([6, 7, 0, 1, 2, 4, 5], 6),
    ([6, 7, 0, 1, 2, 4, 5], 7),
    ([6, 7, 0, 1, 2, 4, 5], 0),
    ([6, 7, 0, 1, 2, 4, 5], 2),
    ([6, 7, 0, 1, 2, 4, 5], 5),
    ([6, 7, 0, 1, 2, 4, 5], 3),
    ([1, 2, 3, 4, 5], 4),
    ([1, 2, 3, 4, 5], 1),
    ([1, 2, 3, 4, 5], 5),
    ([1, 2, 3, 4, 5], 6),
    ([3, 1], 1),
    ([3, 1], 3),
    ([3, 1], 2),
    ([2, 3, 4, 1], 1),
    ([2, 3, 4, 1], 2),
    ([], 5),
    ([3, 4, -2, -1, 2], -2),
    ([3, 4, -2, -1, 2], 3),
]


def main() -> None:
    for nums, target in CASES:
        a = search_one_pass(nums, len(nums), target)
        b = search_pivot(nums, len(nums), target)
        c = search_remap(nums, len(nums), target)
        truth = nums.index(target) if target in nums else -1
        assert a == b == c == truth, (nums, target, a, b, c, truth)
        rendered = "[" + ", ".join(str(x) for x in nums) + "]"
        print(f"{rendered} target={target} -> {a}")


if __name__ == "__main__":
    main()

"""LeetCode #34: Find First and Last Position — known-correct reference oracle.

Algorithmic mirror of search_range.kara (the lower/upper-bound style). Output
format matches line-for-line so the two can be diffed directly. The edge-flag and
find-then-bound variants produce identical output; this oracle additionally
cross-checks all three algorithms agree on every case (and against a brute-force
linear scan of the run's true endpoints).
"""

from __future__ import annotations


# --- Style 1: lower_bound / upper_bound (mirrors search_range.kara) ------------

def lower_bound(nums: list[int], length: int, target: int) -> int:
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums: list[int], length: int, target: int) -> int:
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_bounds(nums: list[int], length: int, target: int) -> tuple[int, int]:
    lo = lower_bound(nums, length, target)
    if lo == length or nums[lo] != target:
        return (-1, -1)
    return (lo, upper_bound(nums, length, target) - 1)


# --- Style 2: single biased edge-finder (mirrors search_range_edge.kara) -------

def search_edge(nums: list[int], length: int, target: int, find_first: bool) -> int:
    lo, hi, ans = 0, length - 1, -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            ans = mid
            if find_first:
                hi = mid - 1
            else:
                lo = mid + 1
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def search_edges(nums: list[int], length: int, target: int) -> tuple[int, int]:
    return (search_edge(nums, length, target, True),
            search_edge(nums, length, target, False))


# --- Style 3: find-one-hit, then bound inward (mirrors search_range_split.kara)-

def find_any(nums: list[int], length: int, target: int) -> int:
    lo, hi = 0, length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def bound_left(nums: list[int], lo: int, hi: int, target: int) -> int:
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bound_right(nums: list[int], lo: int, hi: int, target: int) -> int:
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2
        if nums[mid] > target:
            hi = mid - 1
        else:
            lo = mid
    return lo


def search_split(nums: list[int], length: int, target: int) -> tuple[int, int]:
    h = find_any(nums, length, target)
    if h < 0:
        return (-1, -1)
    return (bound_left(nums, 0, h, target),
            bound_right(nums, h, length - 1, target))


# --- Brute-force ground truth (scan the run's true endpoints) ------------------

def search_brute(nums: list[int], target: int) -> tuple[int, int]:
    first = last = -1
    for i, v in enumerate(nums):
        if v == target:
            if first == -1:
                first = i
            last = i
    return (first, last)


CASES = [
    ([5, 7, 7, 8, 8, 10], 8),
    ([5, 7, 7, 8, 8, 10], 6),
    ([], 0),
    ([1], 1),
    ([1], 0),
    ([2, 2, 2, 2, 2], 2),
    ([2, 2, 2, 2, 2], 1),
    ([2, 2, 2, 2, 2], 3),
    ([4, 4, 5, 6, 7, 9, 9], 4),
    ([4, 4, 5, 6, 7, 9, 9], 9),
    ([4, 4, 5, 6, 7, 9, 9], 5),
    ([4, 4, 5, 6, 7, 9, 9], 8),
    ([-5, -3, -3, -3, 0, 0, 1, 4, 4], -3),
    ([-5, -3, -3, -3, 0, 0, 1, 4, 4], 0),
    ([-5, -3, -3, -3, 0, 0, 1, 4, 4], 4),
    ([-5, -3, -3, -3, 0, 0, 1, 4, 4], -5),
    ([-5, -3, -3, -3, 0, 0, 1, 4, 4], 2),
    ([1, 3], 1),
    ([1, 3], 3),
    ([1, 3], 2),
    ([1, 3], 0),
]


def main() -> None:
    for nums, target in CASES:
        a = search_bounds(nums, len(nums), target)
        b = search_edges(nums, len(nums), target)
        c = search_split(nums, len(nums), target)
        truth = search_brute(nums, target)
        assert a == b == c == truth, (nums, target, a, b, c, truth)
        rendered = "[" + ", ".join(str(x) for x in nums) + "]"
        print(f"{rendered} target={target} -> [{a[0]}, {a[1]}]")


if __name__ == "__main__":
    main()

"""LeetCode #35: Search Insert Position — known-correct reference oracle.

Algorithmic mirror of search_insert.kara (the half-open lower_bound style ★).
Output format matches line-for-line so the two can be diffed directly. The
closed-interval and binary-lifting variants produce identical output; this oracle
additionally cross-checks all three algorithms agree on every case (and against a
brute-force linear scan of the true insertion point).
"""

from __future__ import annotations


# --- Style 1: half-open lower_bound (mirrors search_insert.kara) ---------------

def search_half_open(nums: list[int], length: int, target: int) -> int:
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


# --- Style 2: closed interval, track candidate (mirrors search_insert_closed) --

def search_closed(nums: list[int], length: int, target: int) -> int:
    lo, hi, ans = 0, length - 1, length
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] >= target:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans


# --- Style 3: binary lifting / exponential strides (mirrors search_insert_stride)

def highest_pow2_leq(n: int) -> int:
    p = 1
    while p * 2 <= n:
        p *= 2
    return p


def search_stride(nums: list[int], length: int, target: int) -> int:
    pos = -1
    step = highest_pow2_leq(length)
    while step >= 1:
        nxt = pos + step
        if nxt < length and nums[nxt] < target:
            pos = nxt
        step //= 2
    return pos + 1


# --- Brute-force ground truth (scan for the first index >= target) -------------

def search_brute(nums: list[int], target: int) -> int:
    for i, v in enumerate(nums):
        if v >= target:
            return i
    return len(nums)


CASES = [
    ([1, 3, 5, 6], 5),
    ([1, 3, 5, 6], 2),
    ([1, 3, 5, 6], 7),
    ([1, 3, 5, 6], 0),
    ([], 5),
    ([2], 1),
    ([2], 2),
    ([2], 3),
    ([1, 3, 5, 7, 9], 1),
    ([1, 3, 5, 7, 9], 3),
    ([1, 3, 5, 7, 9], 5),
    ([1, 3, 5, 7, 9], 7),
    ([1, 3, 5, 7, 9], 9),
    ([1, 3, 5, 7, 9], 0),
    ([1, 3, 5, 7, 9], 2),
    ([1, 3, 5, 7, 9], 4),
    ([1, 3, 5, 7, 9], 6),
    ([1, 3, 5, 7, 9], 8),
    ([1, 3, 5, 7, 9], 10),
    ([-9, -4, -1, 0, 3, 8], -9),
    ([-9, -4, -1, 0, 3, 8], -5),
    ([-9, -4, -1, 0, 3, 8], 0),
    ([-9, -4, -1, 0, 3, 8], 8),
    ([-9, -4, -1, 0, 3, 8], 100),
]


def main() -> None:
    for nums, target in CASES:
        a = search_half_open(nums, len(nums), target)
        b = search_closed(nums, len(nums), target)
        c = search_stride(nums, len(nums), target)
        truth = search_brute(nums, target)
        assert a == b == c == truth, (nums, target, a, b, c, truth)
        rendered = "[" + ", ".join(str(x) for x in nums) + "]"
        print(f"{rendered} target={target} -> {a}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""LeetCode #34 bench — Python (mirror of search_range.kara).

Two-bounds style: lower_bound + upper_bound per query over a fixed sorted array
with duplicate runs, TOTAL queries with cycling targets, both endpoints folded
into a checksum. Same sink as every other mirror.
"""


def lower_bound(nums, length, target):
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(nums, length, target):
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    n = 4096
    run = 4
    total = 14000000
    modulus = 1000000007

    nums = [2 * (p // run) for p in range(n)]

    span = 2 * n
    acc = 0
    for k in range(total):
        target = k % span
        lo = lower_bound(nums, n, target)
        first, last = -1, -1
        if lo < n and nums[lo] == target:
            first = lo
            last = upper_bound(nums, n, target) - 1
        acc = (acc * 31 + (first + 1)) % modulus
        acc = (acc * 31 + (last + 1)) % modulus

    print(acc)


if __name__ == "__main__":
    main()

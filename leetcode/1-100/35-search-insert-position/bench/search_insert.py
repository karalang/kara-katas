#!/usr/bin/env python3
"""LeetCode #35 bench — Python (mirror of search_insert.kara).

Half-open lower_bound style: one search_insert (first index >= target) per query
over a fixed strictly-increasing array of distinct values, TOTAL queries with
cycling targets, each index folded into a checksum. Same sink as every other mirror.
"""


def search_insert(nums, length, target):
    lo, hi = 0, length
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    n = 4096
    total = 14000000
    modulus = 1000000007

    nums = [2 * p for p in range(n)]

    span = 2 * n
    acc = 0
    for k in range(total):
        target = k % span
        idx = search_insert(nums, n, target)
        acc = (acc * 31 + idx) % modulus

    print(acc)


if __name__ == "__main__":
    main()

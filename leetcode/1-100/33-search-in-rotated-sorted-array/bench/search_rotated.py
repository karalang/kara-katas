#!/usr/bin/env python3
"""LeetCode #33 bench — Python (mirror of search_rotated.kara).

One-pass modified binary search over a fixed rotated-sorted array, TOTAL searches
with cycling targets, folded into a checksum. Same sink as every other mirror.
"""


def search(nums, length, target):
    lo, hi = 0, length - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        m = nums[mid]
        if m == target:
            return mid
        if nums[lo] <= m:
            if nums[lo] <= target < m:
                hi = mid - 1
            else:
                lo = mid + 1
        elif m < target <= nums[hi]:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def main():
    n = 4096
    rot = 1365
    total = 18000000
    modulus = 1000000007

    nums = [2 * ((p + rot) % n) for p in range(n)]

    span = 2 * n
    acc = 0
    for k in range(total):
        target = k % span
        idx = search(nums, n, target)
        acc = (acc + idx + 2) % modulus

    print(acc)


if __name__ == "__main__":
    main()

"""LeetCode 209 — Minimum Size Subarray Sum (Python mirror / oracle).

Two-pointer sliding window over positive integers: extend right, shrink left
while the window sum stays >= target, track the minimal length. Mirrors the
Kara version.
"""


def min_subarray_len(target, nums):
    n = len(nums)
    left = 0
    total = 0
    best = -1
    for right in range(n):
        total += nums[right]
        while total >= target:
            length = right - left + 1
            if best == -1 or length < best:
                best = length
            total -= nums[left]
            left += 1
    return 0 if best == -1 else best


def report(target, nums):
    print(min_subarray_len(target, nums))


def main():
    report(7, [2, 3, 1, 2, 4, 3])
    report(4, [1, 4, 4])
    report(11, [1, 1, 1, 1, 1, 1, 1, 1])
    report(15, [1, 2, 3, 4, 5])
    report(6, [10])
    report(100, [1, 2, 3])
    report(3, [1, 1, 1, 1, 1])


main()

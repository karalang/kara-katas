"""LeetCode 163 — Missing Ranges (Python mirror / oracle). Premium.

Smallest sorted list of ranges covering every number in [lower, upper] absent
from the sorted array nums. One pass with a `prev` cursor and an upper+1
sentinel. Mirrors the Kāra version.
"""


def fmt_range(lo, hi):
    return str(lo) if lo == hi else f"{lo}->{hi}"


def missing_ranges(nums, lower, upper):
    res = []
    prev = lower - 1
    n = len(nums)
    for i in range(n + 1):
        cur = nums[i] if i < n else upper + 1
        if cur - prev >= 2:
            res.append(fmt_range(prev + 1, cur - 1))
        prev = cur
    return res


def report(nums, lower, upper):
    print(", ".join(missing_ranges(nums, lower, upper)))


def main():
    report([0, 1, 3, 50, 75], 0, 99)
    report([], 1, 1)
    report([], -3, 2)
    report([-1, 0, 1, 2], -1, 2)
    report([1, 3, 5], 1, 5)


main()

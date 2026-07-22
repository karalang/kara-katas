"""LeetCode 167 — Two Sum II - Input Array Is Sorted (Python mirror / oracle).

Two-pointer sweep on the sorted array: advance the left pointer when the pair
sums too low, retreat the right when too high. Returns 1-based indices. Mirrors
the Kāra version.
"""


def two_sum(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return [-1, -1]


def report(nums, target):
    r = two_sum(nums, target)
    print(f"{r[0]} {r[1]}")


def main():
    report([2, 7, 11, 15], 9)
    report([2, 3, 4], 6)
    report([-1, 0], -1)
    report([1, 2, 3, 4, 4], 8)
    report([0, 0, 3, 4, 5, 9], 0)


main()

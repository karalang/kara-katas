"""LeetCode 154 — Find Minimum in Rotated Sorted Array II (Python mirror / oracle).

Binary search comparing nums[mid] to nums[hi]; on a tie shrink hi by one (the
discarded value is duplicated at mid, so the min is never lost). O(log n)
typically, O(n) worst case (all equal). Mirrors the Kāra version.
"""


def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1
    return nums[lo]


def run(nums):
    print(find_min(nums))


def main():
    run([1, 3, 5])
    run([2, 2, 2, 0, 1])
    run([3, 4, 5, 1, 2])
    run([2, 2, 2, 2, 2])
    run([1])
    run([10, 1, 10, 10, 10])


main()

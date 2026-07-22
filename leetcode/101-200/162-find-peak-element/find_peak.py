"""LeetCode 162 — Find Peak Element (Python mirror / oracle).

Binary search on the slope: climb toward a peak (nums[mid] < nums[mid+1] -> go
right, else go left). Returns the same index the Kāra version does.
"""


def find_peak(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo


def run(nums):
    print(find_peak(nums))


def main():
    run([1, 2, 3, 1])
    run([1, 2, 1, 3, 5, 6, 4])
    run([1])
    run([1, 2])
    run([2, 1])
    run([1, 3, 2, 4, 1])


main()

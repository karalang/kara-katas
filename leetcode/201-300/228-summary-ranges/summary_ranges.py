"""LeetCode 228 — Summary Ranges (Python mirror / oracle).

One linear scan over a sorted distinct array; close a run where consecutiveness
breaks, emitting "a" or "a->b". Mirrors the Kara version.
"""


def summary_ranges(nums):
    n = len(nums)
    result = []
    if n == 0:
        return result
    start = nums[0]
    i = 1
    while i <= n:
        if i == n or nums[i] != nums[i - 1] + 1:
            end = nums[i - 1]
            if start == end:
                result.append(f"{start}")
            else:
                result.append(f"{start}->{end}")
            if i < n:
                start = nums[i]
        i += 1
    return result


def report(nums):
    ranges = summary_ranges(nums)
    print(" ".join(ranges) if ranges else "(empty)")


def main():
    report([0, 1, 2, 4, 5, 7])
    report([0, 2, 3, 4, 6, 8, 9])
    report([])
    report([5])
    report([-3, -2, -1, 1, 2])
    report([1, 3, 5, 7])
    report([-1, 0, 1])


main()

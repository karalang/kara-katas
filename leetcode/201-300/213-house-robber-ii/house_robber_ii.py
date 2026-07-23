"""LeetCode 213 — House Robber II (Python mirror / oracle).

Circular constraint = two linear House Robber runs (skip first end or skip last
end); take the larger. Each run is the O(1)-space rolling DP. Mirrors the Kara
version.
"""


def rob_linear(nums, lo, hi):
    prev = 0
    cur = 0
    for i in range(lo, hi):
        take = prev + nums[i]
        nxt = take if take > cur else cur
        prev = cur
        cur = nxt
    return cur


def rob(nums):
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]
    skip_last = rob_linear(nums, 0, n - 1)
    skip_first = rob_linear(nums, 1, n)
    return skip_last if skip_last > skip_first else skip_first


def report(nums):
    print(rob(nums))


def main():
    report([2, 3, 2])
    report([1, 2, 3, 1])
    report([1, 2, 3])
    report([5])
    report([1, 2])
    report([200, 3, 140, 20, 10])
    report([1, 3, 1, 3, 100, 1])


main()

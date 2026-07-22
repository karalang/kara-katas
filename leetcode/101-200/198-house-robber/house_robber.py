"""LeetCode 198 — House Robber (Python mirror / oracle).

O(1)-space DP carrying the best up to i-1 and i-2: cur = max(prev, prev2 + x).
Mirrors the Kāra version.
"""


def rob(nums):
    prev2 = 0
    prev = 0
    for x in nums:
        cur = max(prev, prev2 + x)
        prev2 = prev
        prev = cur
    return prev


def report(nums):
    print(rob(nums))


def main():
    report([1, 2, 3, 1])
    report([2, 7, 9, 3, 1])
    report([5])
    report([])
    report([2, 1, 1, 2, 1, 1])
    report([100, 1, 100])


main()

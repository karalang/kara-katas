"""LeetCode #315: Count of Smaller Numbers After Self — Fenwick tree over ranks.

Reference mirror of count_smaller.kara: compress values to ranks, walk right to
left, prefix-query the ranks strictly below, then point-update the rank.
"""
from bisect import bisect_left


def count_smaller(nums):
    distinct = sorted(set(nums))
    m = len(distinct)
    tree = [0] * (m + 1)
    counts = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        r = bisect_left(distinct, nums[i])
        total = 0
        x = r
        while x > 0:
            total += tree[x]
            x -= x & -x
        counts[i] = total
        x = r + 1
        while x <= m:
            tree[x] += 1
            x += x & -x
    return counts


def fmt(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    cases = [
        [5, 2, 6, 1],
        [-1],
        [-1, -1],
        [],
        [3, 3, 3, 3],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [-10000, 10000, 0, -10000, 7, 7, -3],
        [2, 0, 1],
    ]
    acc = 0
    for c, case in enumerate(cases):
        counts = count_smaller(case)
        for v in counts:
            acc = (acc * 131 + v + 1) % 1000000007
        print(f"case {c}: {fmt(counts)}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()

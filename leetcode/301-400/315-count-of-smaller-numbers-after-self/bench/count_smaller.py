"""Benchmark lane for LeetCode 315 — Python mirror of bench/count_smaller.kara.

Generate N values once, then PASSES Fenwick-tree passes (sort+dedup for the
ranks, then per element a binary search, a prefix query and a point update,
right to left), each after swapping two elements chosen from the checksum.
"""
from bisect import bisect_left

N = 200000
PASSES = 24
MASK = 1073741823


def lcg(s):
    return (s * 1103515245 + 12345) & 0x7FFFFFFF


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


def main():
    seed = 315
    nums = []
    for _ in range(N):
        seed = lcg(seed)
        nums.append(seed % 200001 - 100000)
    checksum = 0
    for _ in range(PASSES):
        i = checksum % N
        j = (checksum * 7 + 13) % N
        nums[i], nums[j] = nums[j], nums[i]
        total = sum(count_smaller(nums))
        checksum = (checksum * 31 + total) & MASK
        nums[i], nums[j] = nums[j], nums[i]
    print(f"checksum {checksum}")


if __name__ == "__main__":
    main()

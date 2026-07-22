"""LeetCode 164 — Maximum Gap (Python mirror / oracle).

Pigeonhole bucket method: bucket width max(1, (hi-lo)//(n-1)) guarantees the
maximum gap spans a bucket boundary, so keep only per-bucket min/max and take the
largest curBucketMin - prevBucketMax. O(n). Mirrors the Kāra version.
"""


def maximum_gap(nums):
    n = len(nums)
    if n < 2:
        return 0
    lo, hi = min(nums), max(nums)
    if lo == hi:
        return 0
    bsize = max(1, (hi - lo) // (n - 1))
    bcount = (hi - lo) // bsize + 1
    used = [False] * bcount
    bmin = [0] * bcount
    bmax = [0] * bcount
    for x in nums:
        idx = (x - lo) // bsize
        if used[idx]:
            bmin[idx] = min(bmin[idx], x)
            bmax[idx] = max(bmax[idx], x)
        else:
            bmin[idx] = bmax[idx] = x
            used[idx] = True
    gap = 0
    prev_max = lo
    for i in range(bcount):
        if used[i]:
            gap = max(gap, bmin[i] - prev_max)
            prev_max = bmax[i]
    return gap


def report(nums):
    print(maximum_gap(nums))


def main():
    report([3, 6, 9, 1])
    report([10, 1])
    report([1])
    report([])
    report([1, 1, 1, 1, 1])
    report([100, 3, 2, 1, 50, 51])
    report([15, 2, 38, 4, 9, 22, 30])


main()

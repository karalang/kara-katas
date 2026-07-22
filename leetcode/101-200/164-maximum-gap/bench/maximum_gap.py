"""LeetCode 164 — Maximum Gap benchmark kernel (Python mirror).

Build-once + punch: LCG-filled N values, call maximum_gap K times perturbing one
element each round. Sink = sum of the K gaps. Identical algorithm to the Kāra /
C / Rust / Go mirrors.
"""


def maximum_gap(nums):
    n = len(nums)
    if n < 2:
        return 0
    lo, hi = nums[0], nums[0]
    for i in range(1, n):
        if nums[i] < lo:
            lo = nums[i]
        if nums[i] > hi:
            hi = nums[i]
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
            if x < bmin[idx]:
                bmin[idx] = x
            if x > bmax[idx]:
                bmax[idx] = x
        else:
            bmin[idx] = bmax[idx] = x
            used[idx] = True
    gap = 0
    prev_max = lo
    for i in range(bcount):
        if used[i]:
            if bmin[i] - prev_max > gap:
                gap = bmin[i] - prev_max
            prev_max = bmax[i]
    return gap


def main():
    n = 1000000
    k = 30
    rng = 1000000000
    nums = [0] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        nums[i] = state % rng
    sink = 0
    for round in range(k):
        idx = (round * 7919) % n
        nums[idx] = (nums[idx] + 1 + round) % rng
        sink += maximum_gap(nums)
    print(sink)


main()

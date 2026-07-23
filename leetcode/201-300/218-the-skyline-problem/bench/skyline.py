"""Benchmark workload for LeetCode #218 — The Skyline Problem (Python; scale lane)."""

import sys


def merge(left, right):
    result = []
    nl = len(left)
    nr = len(right)
    i = 0
    j = 0
    h1 = 0
    h2 = 0
    while i < nl and j < nr:
        if left[i][0] < right[j][0]:
            x = left[i][0]
            h1 = left[i][1]
            i += 1
        elif left[i][0] > right[j][0]:
            x = right[j][0]
            h2 = right[j][1]
            j += 1
        else:
            x = left[i][0]
            h1 = left[i][1]
            h2 = right[j][1]
            i += 1
            j += 1
        maxh = h1 if h1 > h2 else h2
        if not result or result[-1][1] != maxh:
            result.append((x, maxh))
    while i < nl:
        result.append(left[i])
        i += 1
    while j < nr:
        result.append(right[j])
        j += 1
    return result


def skyline(bs, lo, hi):
    if hi - lo == 1:
        b = bs[lo]
        return [(b[0], b[2]), (b[1], 0)]
    mid = lo + (hi - lo) // 2
    left = skyline(bs, lo, mid)
    right = skyline(bs, mid, hi)
    return merge(left, right)


def main():
    n = 24000
    passes = 100
    xr = 200000
    wr = 120
    hr = 1000

    bs = []
    state = 12345
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        left = state % xr
        state = (state * 1103515245 + 12345) & 2147483647
        width = 1 + state % wr
        state = (state * 1103515245 + 12345) & 2147483647
        height = 1 + state % hr
        bs.append((left, left + width, height))

    sink = 0
    for p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = p % n
        b = bs[idx]
        bs[idx] = (b[0], b[1], 1 + state % hr)
        sky = skyline(bs, 0, n)
        for pt in sky:
            sink += pt[0] + pt[1]
    print(sink)


sys.setrecursionlimit(100000)
main()

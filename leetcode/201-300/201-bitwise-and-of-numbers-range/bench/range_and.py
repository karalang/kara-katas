"""Benchmark workload for LeetCode #201 — Bitwise AND of Numbers Range (Python; scale lane)."""


def range_and(left, right):
    lo = left
    hi = right
    shift = 0
    while lo < hi:
        lo >>= 1
        hi >>= 1
        shift += 1
    return lo << shift


def main():
    iters = 20000000
    state = 12345
    sink = 0
    for _ in range(iters):
        state = (state * 1103515245 + 12345) & 2147483647
        x = state
        state = (state * 1103515245 + 12345) & 2147483647
        y = state
        lo = x if x < y else y
        hi = y if x < y else x
        sink += range_and(lo, hi)
    print(sink)


main()

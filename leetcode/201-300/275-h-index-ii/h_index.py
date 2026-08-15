#!/usr/bin/env python3
"""LeetCode 275 — H-Index II. Mirror of the ★ solver.

Same binary search on the index, same half-open invariant (`lo` is a candidate,
`hi` is one past the last), same `n - lo` at the end so that "nothing qualifies"
falls out as 0.
"""


def h_index(citations):
    n = len(citations)
    lo, hi = 0, n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if citations[mid] >= n - mid:
            hi = mid
        else:
            lo = mid + 1
    return n - lo


def show(xs):
    return "[" + ",".join(str(x) for x in xs) + "]"


def main():
    cases = [
        [0, 1, 3, 5, 6],
        [1, 2, 100],
        [0],
        [100],
        [0, 0, 0],
        [5, 5, 5],
        [0, 0, 4, 4],
        [1, 1, 1, 1, 1],
        [0, 1, 2, 3, 4],
    ]
    for c in cases:
        print(f"{show(c)} -> {h_index(c)}")


main()

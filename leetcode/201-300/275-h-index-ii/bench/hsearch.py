#!/usr/bin/env python3
"""Benchmark workload for LeetCode #275 — H-Index II.

Algorithm-for-algorithm mirror of hsearch.kara. Kept as a CORRECTNESS ORACLE,
not a timed lane: Python is excluded from the measured comparison
(KARA_BENCH_INCLUDE_PY defaults to 0 in scripts/bench-lib.sh).
"""

SIZE = 262144
QUERIES = 6000000


def h_index_prefix(citations, n):
    lo, hi = 0, n
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if citations[mid] >= n - mid:
            hi = mid
        else:
            lo = mid + 1
    return n - lo


def main():
    citations = []
    state, cur = 275275, 0
    for _ in range(SIZE):
        state = (state * 1103515245 + 12345) & 2147483647
        cur += (state // 256) % 3
        citations.append(cur)
    top = citations[SIZE - 1]

    sink = 0
    for _ in range(QUERIES):
        state = (state * 1103515245 + 12345) & 2147483647
        n = 1 + (state // 256) % SIZE
        sink = (sink * 131 + h_index_prefix(citations, n)) % 1000000007

    print(sink)
    print(f"size {SIZE} queries {QUERIES} top {top}")


main()

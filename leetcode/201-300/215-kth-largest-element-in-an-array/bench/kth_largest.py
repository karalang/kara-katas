"""Benchmark workload for LeetCode #215 — Kth Largest Element in an Array (Python; scale lane)."""

import sys


def partition(a, lo, hi):
    pivot = a[hi]
    i = lo
    j = lo
    while j < hi:
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
        j += 1
    a[i], a[hi] = a[hi], a[i]
    return i


def quickselect(a, lo, hi, target):
    if lo == hi:
        return a[lo]
    p = partition(a, lo, hi)
    if p == target:
        return a[p]
    if target < p:
        return quickselect(a, lo, p - 1, target)
    return quickselect(a, p + 1, hi, target)


def main():
    n = 120000
    passes = 420
    k = 40000
    target = n - k

    a = [0] * n
    state = 12345
    sink = 0
    for _ in range(passes):
        for i in range(n):
            state = (state * 1103515245 + 12345) & 2147483647
            a[i] = state
        sink += quickselect(a, 0, n - 1, target)
    print(sink)


sys.setrecursionlimit(200000)
main()

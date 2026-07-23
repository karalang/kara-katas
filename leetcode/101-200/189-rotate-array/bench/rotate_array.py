"""Benchmark workload for LeetCode #189 — Rotate Array (Python; scale lane)."""

import sys


def reverse_range(a, lo, hi):
    i = lo
    j = hi
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def rotate(a, k):
    n = len(a)
    if n == 0:
        return
    kk = k % n
    reverse_range(a, 0, n - 1)
    reverse_range(a, 0, kk - 1)
    reverse_range(a, kk, n - 1)


def checksum(a, n):
    chk = 0
    for i in range(n):
        chk = ((chk * 131) + a[i]) & 2147483647
    return chk


def main():
    n = 30000
    passes = 4000
    a = [0] * n
    state = 12345
    for b in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        a[b] = state
    sink = 0
    for _ in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        k = state % n
        rotate(a, k)
        sink += checksum(a, n)
    print(sink)


main()

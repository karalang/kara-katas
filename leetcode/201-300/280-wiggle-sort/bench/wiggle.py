#!/usr/bin/env python3
"""LeetCode 280 bench mirror — Python. Same greedy, refresh and sink."""
N = 2000000
ROUNDS = 30


def wiggle_sort(a):
    for i in range(1, len(a)):
        if i % 2 == 1:
            if a[i] < a[i - 1]:
                a[i], a[i - 1] = a[i - 1], a[i]
        else:
            if a[i] > a[i - 1]:
                a[i], a[i - 1] = a[i - 1], a[i]


def main():
    src = [0] * N
    seed = 20260818
    for i in range(N):
        seed = (seed * 1103515245 + 12345) % 2147483648
        src[i] = seed % 1000003
    sink = 0
    for _ in range(ROUNDS):
        work = list(src)
        wiggle_sort(work)
        h = 0
        for v in work:
            h = (h * 31 + v) % 1000000007
        sink = (sink + h) % 1000000007
    print(sink)


main()

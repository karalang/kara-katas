#!/usr/bin/env python3
"""LeetCode 283 bench mirror — Python. Same cursor, refresh and sink."""
N = 2000000
ROUNDS = 60


def move_zeroes(a, st):
    write = 0
    for i in range(len(a)):
        if a[i] != 0:
            a[write] = a[i]
            st[0] += 1
            write += 1
    while write < len(a):
        a[write] = 0
        st[0] += 1
        write += 1


def main():
    seed = 20260821
    src = [0] * N
    for i in range(N):
        seed = (seed * 1103515245 + 12345) % 2147483648
        src[i] = 0 if seed % 2 == 0 else seed % 100003
    sink = total = 0
    for _ in range(ROUNDS):
        work = list(src)
        st = [0]
        move_zeroes(work, st)
        total += st[0]
        h = 0
        for v in work:
            h = (h * 31 + v) % 1000000007
        sink = (sink + h) % 1000000007
    print(sink, total)


main()

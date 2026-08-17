#!/usr/bin/env python3
"""LeetCode 277 bench mirror — Python. Same algorithm; included for corpus
completeness rather than because the number is interesting."""

N = 2500000
INSTANCES = 64


def knows(star, a, b):
    if b == star:
        return True
    if a == star:
        return False
    return ((a * 1103515245 + b * 12345) % 2147483647) % 2 == 0


def find_celebrity(n, star):
    cand = 0
    for i in range(1, n):
        if knows(star, cand, i):
            cand = i
    for j in range(n):
        if j != cand:
            if knows(star, cand, j):
                return -1
            if not knows(star, j, cand):
                return -1
    return cand


def main():
    sink = 0
    for i in range(INSTANCES):
        star = (i * 7919) % N
        sink = (sink + (i * 1000003 + find_celebrity(N, star)) % 1000000007) % 1000000007
    print(sink)


main()

#!/usr/bin/env python3
"""LeetCode 279 bench mirror — Python. Same DP, same checksum."""
N = 300000


def main():
    least = [0] * (N + 1)
    for i in range(1, N + 1):
        best = i
        j = 1
        while j * j <= i:
            cand = least[i - j * j] + 1
            if cand < best:
                best = cand
            j += 1
        least[i] = best
    s = 0
    for k in range(N + 1):
        s = (s * 31 + least[k]) % 1000000007
    print((s * 10 + least[N]) % 1000000007)


main()

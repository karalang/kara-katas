#!/usr/bin/env python3
"""LeetCode 276 bench mirror — brute-force enumeration, Python.

Same algorithm as paint_enum.kara; sequential over the 16 prefixes. Included for
completeness of the corpus, not because the number is interesting — pure-Python
enumeration of 67M paintings is roughly three orders of magnitude off the
compiled lanes.
"""

N = 13
K = 4


def count_prefix(p0, p1):
    c = [0] * N
    c[0] = p0
    c[1] = p1
    count = 0
    while True:
        ok = True
        for i in range(2, N):
            if c[i] == c[i - 1] == c[i - 2]:
                ok = False
        if ok:
            count += 1
        p = N - 1
        while p >= 2 and c[p] == K - 1:
            c[p] = 0
            p -= 1
        if p < 2:
            break
        c[p] += 1
    return count


def main():
    total = 0
    for pre in range(K * K):
        total += count_prefix(pre // K, pre % K)
    print(total)


main()

"""Benchmark workload — Scramble String (LeetCode #87), SEQ lane.

Python mirror of bench/scramble_string.kara. Each iteration builds a length-12 string
and a coprime-step permutation of it, runs the O(n^4) top-down memoized scramble, and
folds the filled memo state into a work-sensitive checksum added to an associative sum.
Runs a smaller K (pure-Python is slow); timed separately, NOT cross-checked.
See ../README.md.
"""

import sys


def scramble(s1, i1, s2, i2, length, memo, n):
    if length == 0:
        return True
    key = (i1 * n + i2) * (n + 1) + length
    if memo[key] != -1:
        return memo[key] == 1
    equal = True
    for k in range(length):
        if s1[i1 + k] != s2[i2 + k]:
            equal = False
            break
    if equal:
        memo[key] = 1
        return True
    counts = [0] * 26
    for k in range(length):
        counts[s1[i1 + k] - 97] += 1
        counts[s2[i2 + k] - 97] -= 1
    for c in range(26):
        if counts[c] != 0:
            memo[key] = 0
            return False
    for split in range(1, length):
        if (scramble(s1, i1, s2, i2, split, memo, n)
                and scramble(s1, i1 + split, s2, i2 + split, length - split, memo, n)):
            memo[key] = 1
            return True
        if (scramble(s1, i1, s2, i2 + length - split, split, memo, n)
                and scramble(s1, i1 + split, s2, i2, length - split, memo, n)):
            memo[key] = 1
            return True
    memo[key] = 0
    return False


def one(length, seed):
    s1 = [97 + (j % 8) for j in range(length)]
    s2 = [s1[(j * 5 + seed) % length] for j in range(length)]
    cells = length * length * (length + 1)
    memo = [-1] * cells
    r = 1 if scramble(s1, 0, s2, 0, length, memo, length) else 0
    h = r
    for i in range(cells):
        h = (h * 131 + (memo[i] + 2)) % 1000000007
    return h


def main():
    length = 12
    total = 4000
    total_sum = 0
    for k in range(total):
        total_sum += one(length, k)
    print(total_sum)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()

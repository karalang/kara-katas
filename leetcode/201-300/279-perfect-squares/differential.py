#!/usr/bin/env python3
"""LeetCode 279 — differential harness. Mirror of differential.kara.

Three unrelated derivations: bottom-up DP, BFS shortest path, and the closed
form from Lagrange's four-square theorem plus Legendre's three-square theorem.
"""


def dp_least(n, table):
    while len(table) <= n:
        i = len(table)
        best = i
        j = 1
        while j * j <= i:
            cand = table[i - j * j] + 1
            if cand < best:
                best = cand
            j += 1
        table.append(best)
    return table[n]


def bfs_least(n):
    if n <= 0:
        return 0
    seen = [False] * (n + 1)
    frontier = [n]
    seen[n] = True
    level = 0
    while frontier:
        level += 1
        nxt_level = []
        for cur in frontier:
            j = 1
            while j * j <= cur:
                nxt = cur - j * j
                if nxt == 0:
                    return level
                if not seen[nxt]:
                    seen[nxt] = True
                    nxt_level.append(nxt)
                j += 1
        frontier = nxt_level
    return 0


def is_square(n):
    if n < 0:
        return False
    r = 0
    while r * r < n:
        r += 1
    return r * r == n


def theory_least(n):
    if n <= 0:
        return 0
    if is_square(n):
        return 1
    m = n
    while m % 4 == 0:
        m //= 4
    if m % 8 == 7:
        return 4
    i = 1
    while i * i <= n:
        if is_square(n - i * i):
            return 2
        i += 1
    return 3


def count_legendre(limit):
    c = 0
    for n in range(1, limit + 1):
        m = n
        while m % 4 == 0:
            m //= 4
        if m % 8 == 7:
            c += 1
    return c


def main():
    limit = 1200
    table = [0]
    ones = twos = threes = fours = 0
    dp_vs_bfs = dp_vs_theory = over_four = digest = 0

    for n in range(1, limit + 1):
        a = dp_least(n, table)
        b = bfs_least(n)
        c = theory_least(n)
        if a != b:
            dp_vs_bfs += 1
        if a != c:
            dp_vs_theory += 1
        if a > 4:
            over_four += 1
        if a == 1:
            ones += 1
        elif a == 2:
            twos += 1
        elif a == 3:
            threes += 1
        elif a == 4:
            fours += 1
        digest = (digest * 131 + a) % 1000000007

    legendre = count_legendre(limit)
    print(f"n from 1 to {limit}")
    print(f"answers: 1 -> {ones}, 2 -> {twos}, 3 -> {threes}, 4 -> {fours}")
    print(f"Lagrange violations (an answer above 4) {over_four}")
    print(f"Legendre numbers counted independently {legendre}")
    print(f"...and answers of 4 {fours} — these must be equal")
    print(f"digest {digest}")
    print(f"DP vs BFS {dp_vs_bfs}")
    print(f"DP vs closed form {dp_vs_theory}")


main()

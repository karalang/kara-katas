"""LeetCode #343: Integer Break — Python mirror.

Mirrors integer_break.kara (dynamic programming over every total) and
integer_break_greedy.kara (take threes while more than four is left).
Prints the same lines; run with `--greedy` for the greedy arm.
"""
import sys


def integer_break(n):
    best = [0] * (n + 1)
    for i in range(2, n + 1):
        for j in range(1, i):
            whole = j * (i - j)
            broken = j * best[i - j]
            if whole > best[i]:
                best[i] = whole
            if broken > best[i]:
                best[i] = broken
    return best[n]


def integer_break_greedy(n):
    if n <= 3:
        return n - 1
    rest = n
    product = 1
    while rest > 4:
        product *= 3
        rest -= 3
    return product * rest


SOLVE = integer_break_greedy if "--greedy" in sys.argv else integer_break


def main():
    print(f"2 -> {SOLVE(2)}")
    print(f"10 -> {SOLVE(10)}")
    total = 0
    for n in range(2, 59):
        p = SOLVE(n)
        print(f"{n} -> {p}")
        total += p
    print(f"sum over 2..58: {total}")
    print(f"100 -> {SOLVE(100)}")
    print(f"119 -> {SOLVE(119)}")


main()

"""LeetCode 201 — Bitwise AND of Numbers Range (Python mirror / oracle).

The AND over [left, right] is their common binary prefix: shift both right until
equal, then shift back. Mirrors the Kāra version.
"""


def range_and(left, right):
    lo, hi = left, right
    shift = 0
    while lo < hi:
        lo >>= 1
        hi >>= 1
        shift += 1
    return lo << shift


def report(left, right):
    print(range_and(left, right))


def main():
    report(5, 7)
    report(0, 0)
    report(1, 2147483647)
    report(12, 15)
    report(6, 6)
    report(600000000, 2147483645)


main()

"""LeetCode 172 — Factorial Trailing Zeroes (Python mirror / oracle).

Count factors of 5 in n!: sum ⌊n/5⌋ + ⌊n/25⌋ + … by repeatedly dividing (every
intermediate stays below n, so no overflow). Mirrors the Kāra version.
"""


def trailing_zeroes(n):
    count = 0
    m = n // 5
    while m > 0:
        count += m
        m //= 5
    return count


def report(n):
    print(trailing_zeroes(n))


def main():
    report(3)
    report(5)
    report(0)
    report(10)
    report(25)
    report(100)
    report(1000)
    report(10000)


main()

"""LeetCode 231 — Power of Two (Python mirror / oracle).

A positive power of two has one set bit, so n & (n-1) == 0. Mirrors the Kara
version.
"""


def is_power_of_two(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def report(n):
    print("true" if is_power_of_two(n) else "false")


def main():
    report(1)
    report(2)
    report(16)
    report(3)
    report(0)
    report(-16)
    report(6)
    report(1024)
    report(2147483648)
    report(1073741824)
    report(100)


main()

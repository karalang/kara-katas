"""LeetCode 263 — Ugly Number (Python mirror / oracle).

Mirrors ugly_number.kara algorithm-for-algorithm: divide out every 2, then
every 3, then every 5, and require a residue of 1 — behind the n <= 0 guard,
without which the loop on n = 0 never terminates.
"""


def is_ugly(n):
    if n <= 0:
        return False
    m = n
    while m % 2 == 0:
        m //= 2
    while m % 3 == 0:
        m //= 3
    while m % 5 == 0:
        m //= 5
    return m == 1


def report(n):
    print(f"{n} -> {'true' if is_ugly(n) else 'false'}")


def main():
    for n in (1, 6, 8, 14, 0, -6, -1, 2, 3, 5, 7, 30, 1024, 59049, 9765625,
              2147483647, 1259712, 1259711):
        report(n)


main()

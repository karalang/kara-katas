"""LeetCode 168 — Excel Sheet Column Title (Python mirror / oracle).

Bijective base-26: subtract 1 before each digit to shift 1..26 -> 0..25 (A..Z),
then divide by 26; digits emerge least-significant first, so reverse. Mirrors the
Kāra version.
"""


def column_title(column_number):
    chars = []
    x = column_number
    while x > 0:
        x -= 1
        chars.append(chr(ord("A") + x % 26))
        x //= 26
    return "".join(reversed(chars))


def report(n):
    print(column_title(n))


def main():
    report(1)
    report(26)
    report(27)
    report(28)
    report(52)
    report(701)
    report(702)
    report(703)
    report(2147483647)


main()

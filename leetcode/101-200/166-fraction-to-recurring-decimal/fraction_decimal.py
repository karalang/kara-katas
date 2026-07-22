"""LeetCode 166 — Fraction to Recurring Decimal (Python mirror / oracle).

Long division: emit the integer part, then generate fractional digits from the
running remainder, recording each remainder's digit position so a recurrence can
be parenthesised. Mirrors the Kāra version.
"""


def fraction(num, den):
    if num == 0:
        return "0"
    out = ""
    if (num < 0 < den) or (den < 0 < num):
        out += "-"
    n, d = abs(num), abs(den)
    out += str(n // d)
    rem = n % d
    if rem == 0:
        return out
    out += "."
    digits = []
    pos = {}
    repeat_start = -1
    while rem != 0:
        if rem in pos:
            repeat_start = pos[rem]
            break
        pos[rem] = len(digits)
        rem *= 10
        digits.append(rem // d)
        rem %= d
    parts = []
    for i in range(len(digits)):
        if i == repeat_start:
            parts.append("(")
        parts.append(str(digits[i]))
    if repeat_start >= 0:
        parts.append(")")
    return out + "".join(parts)


def report(num, den):
    print(fraction(num, den))


def main():
    report(1, 2)
    report(2, 1)
    report(2, 3)
    report(4, 333)
    report(1, 6)
    report(-50, 8)
    report(1, -3)
    report(0, 5)
    report(7, 12)
    report(22, 7)


main()

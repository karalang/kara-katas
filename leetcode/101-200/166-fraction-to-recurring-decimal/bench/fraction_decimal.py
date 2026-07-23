"""Benchmark workload for LeetCode #166 — Fraction to Recurring Decimal (Python; scale lane)."""


def frac_checksum(num, den):
    rem = num % den
    checksum = 0
    if rem == 0:
        return 0
    pos = {}
    count = 0
    while rem != 0:
        if rem in pos:
            rem = 0  # cycle closed — stop
        else:
            pos[rem] = count
            rem *= 10
            digit = rem // den
            checksum += digit
            rem %= den
            count += 1
    return checksum


def main():
    passes = 500000
    state = 12345
    sink = 0
    for _p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        num = state % 1000000
        state = (state * 1103515245 + 12345) & 2147483647
        den = 2 + (state % 1023)
        sink += frac_checksum(num, den)
    print(sink)


main()

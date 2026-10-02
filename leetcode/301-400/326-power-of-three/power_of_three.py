"""LeetCode #326: Power of Three — Python mirror.

Mirrors power_of_three.kara (divide out every factor of 3) and
power_of_three_divisor.kara (3^19 is divisible only by powers of three).
Prints the same lines; run with `--divisor` for the divisor arm.
"""
import sys

MAX_POWER = 1162261467  # 3^19, the largest power of three below 2^31


def is_power_of_three(n):
    if n <= 0:
        return False
    m = n
    while m % 3 == 0:
        m //= 3
    return m == 1


def is_power_of_three_divisor(n):
    return n > 0 and MAX_POWER % n == 0


SOLVE = is_power_of_three_divisor if "--divisor" in sys.argv else is_power_of_three


def show(b):
    return "true" if b else "false"


def report(n):
    print(f"{n} -> {show(SOLVE(n))}")


I32_MIN = -2147483648
I32_MAX = 2147483647


def main():
    for n in (27, 0, -1, 1, 3, 9, 45, -3, -27, 2, 243,
              1162261467, 1162261466, 1162261468, I32_MAX, I32_MIN):
        report(n)

    p = 1
    hits = 0
    misses = 0
    for _ in range(20):
        if SOLVE(p):
            hits += 1
        if SOLVE(p - 1) or SOLVE(p + 1):
            if p > 3:
                misses += 1
        p *= 3
    print(f"powers 3^0..3^19: {hits} of 20 accepted, {misses} neighbours above 3 accepted")

    count = 0
    total = 0
    for n in range(-1000, 1000001):
        if SOLVE(n):
            count += 1
            total += n
    print(f"[-1000, 1000000]: {count} powers, sum {total}")


main()

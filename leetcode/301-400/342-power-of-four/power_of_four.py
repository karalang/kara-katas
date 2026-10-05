"""LeetCode #342: Power of Four — Python mirror.

Mirrors power_of_four.kara (one set bit, in an even position) and
power_of_four_divide.kara (divide out every factor of 4). Prints the same
lines; run with `--divide` for the divide arm.
"""
import sys


def is_power_of_four(n):
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0


def is_power_of_four_divide(n):
    if n <= 0:
        return False
    m = n
    while m % 4 == 0:
        m //= 4
    return m == 1


SOLVE = is_power_of_four_divide if "--divide" in sys.argv else is_power_of_four


def show(b):
    return "true" if b else "false"


def report(n):
    print(f"{n} -> {show(SOLVE(n))}")


I32_MIN = -2147483648
I32_MAX = 2147483647


def main():
    for n in (16, 5, 1, 0, 4, 64, 2, 8, 32, -4, -16,
              1073741824, 1073741823, 1073741825, 536870912, I32_MAX, I32_MIN):
        report(n)

    p = 1
    fours = 0
    neighbours = 0
    for k in range(31):
        if SOLVE(p):
            fours += 1
            if k % 2 == 1:
                print(f"wrong: 2^{k} accepted")
        elif k % 2 == 0:
            print(f"wrong: 2^{k} rejected")
        if p > 4 and (SOLVE(p - 1) or SOLVE(p + 1)):
            neighbours += 1
        if k < 30:
            p *= 2
    print(f"powers 2^0..2^30: {fours} powers of four, {neighbours} neighbours above 4 accepted")

    count = 0
    total = 0
    for n in range(-1000, 1000001):
        if SOLVE(n):
            count += 1
            total += n
    print(f"[-1000, 1000000]: {count} powers, sum {total}")


main()

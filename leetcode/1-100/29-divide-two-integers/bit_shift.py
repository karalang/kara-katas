"""LeetCode #29: Divide Two Integers — bit-shift long division.

Algorithmic mirror of bit_shift.kara. Output format matches line-for-line so
the two can be diffed directly.

Note: this re-implements truncating division with shifts rather than using
Python's `//` (which floors toward negative infinity) — the whole point of the
kata is to divide without `*`, `/`, or `%`, and to truncate toward zero.
"""

from __future__ import annotations


def divide(dividend: int, divisor: int) -> int:
    int_max = 2147483647
    int_min = -2147483648

    # The sole result that overflows the signed 32-bit range — saturate.
    if dividend == int_min and divisor == -1:
        return int_max

    # Sign of the quotient is the XOR of the operand signs.
    negative = (dividend < 0) != (divisor < 0)

    a = abs(dividend)
    b = abs(divisor)

    result = 0
    while a >= b:
        # Largest shifted divisor that still fits under the remainder.
        temp = b
        multiple = 1
        while a >= (temp << 1):
            temp <<= 1
            multiple <<= 1
        a -= temp
        result += multiple

    return -result if negative else result


def main() -> None:
    print(divide(10, 3))            # 3
    print(divide(7, -3))            # -2
    print(divide(-2147483648, -1))  # 2147483647 (overflow → clamp)
    print(divide(-2147483648, 1))   # -2147483648
    print(divide(-2147483648, 2))   # -1073741824
    print(divide(2147483647, 1))    # 2147483647
    print(divide(0, 5))             # 0
    print(divide(1, 1))             # 1
    print(divide(-7, -3))           # 2
    print(divide(15, 4))            # 3
    print(divide(-15, 4))           # -3
    print(divide(1, -1))            # -1
    print(divide(-2147483648, -2))  # 1073741824


if __name__ == "__main__":
    main()

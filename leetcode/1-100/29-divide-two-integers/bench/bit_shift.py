"""Benchmark workload — bit-shift long division, LeetCode #29.

Algorithmic mirror of bench/bit_shift.kara. See ../README.md § Benchmarks for
the choice of N and the LCG input. Truncating division is re-implemented with
shifts (not Python's flooring `//`) so the sink matches the compiled mirrors.
"""

from __future__ import annotations


def divide(dividend: int, divisor: int) -> int:
    int_max = 2147483647
    int_min = -2147483648
    if dividend == int_min and divisor == -1:
        return int_max
    negative = (dividend < 0) != (divisor < 0)
    a = dividend if dividend >= 0 else -dividend
    b = divisor if divisor >= 0 else -divisor
    result = 0
    while a >= b:
        temp = b
        multiple = 1
        while a >= (temp << 1):
            temp <<= 1
            multiple <<= 1
        a -= temp
        result += multiple
    return -result if negative else result


def main() -> None:
    n = 5_000_000
    state = 1
    total = 0
    for _ in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        dividend = state - 1073741824
        state = (state * 1103515245 + 12345) % 2147483648
        divisor = (state % 2000) - 1000
        if divisor == 0:
            divisor = 1
        total += divide(dividend, divisor)
    print(total)


if __name__ == "__main__":
    main()

"""LeetCode #50: Pow(x, n) — recursive divide-and-conquer (exponentiation by squaring).

Algorithmic mirror of recursive.kara. `fast_pow` recurses on the halved exponent
and squares the partial power on the way back up — the SAME sequence of IEEE-754
multiplications, in the SAME order, that recursive.kara performs — so the f64
results are bit-for-bit identical, not merely close.

Formatting: Kāra prints f64 with Rust's `Display` — the shortest round-trip
decimal, in plain (never scientific) notation, with a bare integer for
integer-valued floats (`1024`, not `1024.0`). `kfmt` reproduces that exactly so
this oracle diffs byte-for-byte against `karac run` / `karac build` output.
"""

from __future__ import annotations

import math
from decimal import Decimal


def kfmt(x: float) -> str:
    """Format an f64 the way Kāra (Rust `Display`) does: shortest round-trip,
    plain decimal, no trailing `.0`."""
    if x == 0.0:
        return "-0" if math.copysign(1.0, x) < 0 else "0"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    s = repr(x)                       # Python's shortest round-trip repr
    if "e" in s or "E" in s:          # expand scientific notation to plain decimal
        s = format(Decimal(s), "f")
    if "." in s:                      # drop the fractional part of integer-valued floats
        s = s.rstrip("0").rstrip(".")
    return s


def fast_pow(x: float, n: int) -> float:
    if n == 0:
        return 1.0
    half = fast_pow(x, n // 2)        # recurse on the halved exponent
    if n % 2 == 0:
        return half * half            # even: square the partial power
    return half * half * x            # odd: square, then fold in one more x


def my_pow(x: float, n: int) -> float:
    if n < 0:
        return 1.0 / fast_pow(x, -n)  # x^n = 1 / x^(-n)
    return fast_pow(x, n)


def main() -> None:
    print(kfmt(my_pow(2.0, 10)))           # 1024
    print(kfmt(my_pow(2.0, -2)))           # 0.25
    print(kfmt(my_pow(2.0, 0)))            # 1
    print(kfmt(my_pow(2.0, -3)))           # 0.125
    print(kfmt(my_pow(-2.0, 3)))           # -8
    print(kfmt(my_pow(0.5, 4)))            # 0.0625
    print(kfmt(my_pow(3.0, 5)))            # 243
    print(kfmt(my_pow(2.0, 30)))           # 1073741824
    print(kfmt(my_pow(2.0, -10)))          # 0.0009765625
    print(kfmt(my_pow(10.0, 4)))           # 10000
    print(kfmt(my_pow(1.0, 2147483647)))   # 1
    print(kfmt(my_pow(1.0, -2147483648)))  # 1
    print(kfmt(my_pow(2.0, -2147483648)))  # 0
    print(kfmt(my_pow(-1.0, 2147483647)))  # -1
    print(kfmt(my_pow(0.5, -3)))           # 8


if __name__ == "__main__":
    main()

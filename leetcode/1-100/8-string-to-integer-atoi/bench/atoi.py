"""Benchmark workload — one-pass atoi (LeetCode #8). Python mirror of
bench/atoi.kara. Same N, K, same input set, same sink formula — see
that file's header for the workload rationale.

Python's int is arbitrary-precision, so the i32 overflow rails are
expressed as constants and the result is widened to int. The byte
walk uses `s.encode('ascii')` rather than `ord(c)` per char so the
inner loop stays in the C `bytes` machinery.
"""

from __future__ import annotations

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)
MAX_DIV = INT_MAX // 10

SPACE = ord(' ')
PLUS  = ord('+')
MINUS = ord('-')
ZERO  = ord('0')
NINE  = ord('9')


def my_atoi(s: str) -> int:
    bytes_ = s.encode('ascii')
    n = len(bytes_)

    i = 0
    while i < n and bytes_[i] == SPACE:
        i += 1

    sign = 1
    if i < n and bytes_[i] == PLUS:
        i += 1
    elif i < n and bytes_[i] == MINUS:
        sign = -1
        i += 1

    result = 0
    while i < n:
        b = bytes_[i]
        if b < ZERO or b > NINE:
            break
        digit = b - ZERO
        if result > MAX_DIV or (result == MAX_DIV and digit > 7):
            return INT_MAX if sign == 1 else INT_MIN
        result = result * 10 + digit
        i += 1

    return sign * result


def main() -> None:
    n = 8
    k_iters = 10_000_000

    inputs = [
        "42",
        "   -42",
        "4193 with words",
        "91283472332",
        "+1",
        "  0000000000012345678",
        "-2147483648",
        "  -0012a42",
    ]

    total = 0
    for k in range(k_iters):
        total += my_atoi(inputs[k % n])
    print(total)


if __name__ == "__main__":
    main()

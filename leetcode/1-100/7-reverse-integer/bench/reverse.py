"""Benchmark workload — pop-and-push Reverse Integer. Python mirror of
bench/reverse.kara. Same N, K, same LCG-style input fill, same sink
formula — see that file's header for the workload rationale.

Python's int is arbitrary-precision, so the i32 overflow rails are
expressed as constants and the inputs are normalized to the signed
32-bit range with a sign-bit mask. `c_div` / `c_mod` keep truncated
division semantics so the algorithm matches the Kāra and Rust shapes
on negative inputs.
"""

from __future__ import annotations

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)
MAX_DIV = INT_MAX // 10
MIN_DIV = -(INT_MAX // 10) - 1


def c_div(a: int, b: int) -> int:
    q, r = divmod(a, b)
    if r != 0 and (a < 0) != (b < 0):
        q += 1
    return q


def c_mod(a: int, b: int) -> int:
    return a - c_div(a, b) * b


def reverse(x: int) -> int:
    result = 0
    while x != 0:
        digit = c_mod(x, 10)
        if result > MAX_DIV or (result == MAX_DIV and digit > 7):
            return 0
        if result < MIN_DIV or (result == MIN_DIV and digit < -8):
            return 0
        result = result * 10 + digit
        x = c_div(x, 10)
    return result


def to_i32(v: int) -> int:
    # Truncate to low 32 bits, then re-interpret as signed two's complement.
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def main() -> None:
    n = 1024
    k_iters = 50_000_000

    inputs = [to_i32(i * 2_654_435_769 + 305_419_896) for i in range(n)]

    total = 0
    for k in range(k_iters):
        total += reverse(inputs[k % n])
    print(total)


if __name__ == "__main__":
    main()

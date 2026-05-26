"""Benchmark workload — half-reverse Palindrome Number. Python mirror
of bench/palindrome.kara. Same N, K, same LCG fill + every-16th
manufactured 8-digit palindrome, same sink formula — see that file's
header for the workload rationale.

Python's int is arbitrary-precision, so inputs are normalized into the
signed 32-bit range with a sign-bit mask via `to_i32`. Unlike kata #7,
the early `x < 0` reject means the palindrome loop only ever sees
non-negative `x`, so Python's floor `//` and Kāra's truncated `/`
produce the same results — no c_div / c_mod helpers needed.
"""

from __future__ import annotations

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)


def is_palindrome(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reversed_ = 0
    while x > reversed_:
        reversed_ = reversed_ * 10 + x % 10
        x = x // 10
    return x == reversed_ or x == reversed_ // 10


def to_i32(v: int) -> int:
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def manufacture_palindrome(v32: int) -> int:
    lo = -v32 if v32 < 0 else v32
    four_raw = lo % 10000
    four = four_raw + 1000 if four_raw < 1000 else four_raw
    d0 = four % 10
    d1 = (four // 10) % 10
    d2 = (four // 100) % 10
    d3 = (four // 1000) % 10
    rev = d0 * 1000 + d1 * 100 + d2 * 10 + d3
    return four * 10000 + rev


def main() -> None:
    n = 1024
    k_iters = 50_000_000

    inputs: list[int] = []
    for i in range(n):
        v32 = to_i32(i * 2_654_435_769 + 305_419_896)
        if i % 16 == 0:
            inputs.append(manufacture_palindrome(v32))
        else:
            inputs.append(v32)

    total = 0
    for k in range(k_iters):
        x = inputs[k % n]
        if is_palindrome(x):
            total += 1
    print(total)


if __name__ == "__main__":
    main()

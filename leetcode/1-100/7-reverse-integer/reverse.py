# LeetCode #7: Reverse Integer — Python mirror of reverse.kara.
#
# Same pop-and-push algorithm with the same INT_MAX / INT_MIN rails.
# Python's `%` and `//` follow Python semantics (floor division, mod
# matches the divisor's sign), which differs from Kāra's C/Rust-style
# truncated division. To keep the algorithm structurally identical
# across both files, we use `math.fmod` + `int(math.trunc(x / 10))`
# emulation via the `c_div` / `c_mod` helpers below.

import math

INT_MAX = 2**31 - 1   # 2_147_483_647
INT_MIN = -(2**31)    # -2_147_483_648
MAX_DIV = INT_MAX // 10
MIN_DIV = -(INT_MAX // 10) - 1   # matches truncated-div semantics for INT_MIN/10

def c_div(a: int, b: int) -> int:
    # Truncated division — rounds toward zero, matching C/Rust/Kāra.
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

def report(x: int) -> None:
    print(reverse(x))

def main() -> None:
    report(123)
    report(-123)
    report(120)
    report(0)
    report(1)
    report(-1)
    report(10)
    report(-10)
    report(1534236469)
    report(-2147483648)
    report(2147483647)
    report(1463847412)
    report(-1463847412)
    report(1463847413)

if __name__ == "__main__":
    main()

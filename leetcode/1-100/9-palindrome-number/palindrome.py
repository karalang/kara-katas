# LeetCode #9: Palindrome Number — Python mirror of palindrome.kara.
#
# Same half-reverse algorithm. Unlike kata #7 (Reverse Integer), this
# kata's early `x < 0` reject means the loop body only ever sees
# non-negative values, so Kāra's truncated `%` / `/` and Python's
# floor `%` / `//` produce the same results — no c_div / c_mod
# helpers needed here.

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)


def is_palindrome(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reversed_ = 0
    while x > reversed_:
        reversed_ = reversed_ * 10 + x % 10
        x = x // 10
    # Even-digit:  x == reversed_       (e.g. 1221 → x=12, reversed_=12)
    # Odd-digit:   x == reversed_ // 10 (middle digit drops out — 12321 → x=12, reversed_=123)
    return x == reversed_ or x == reversed_ // 10


def report(x: int) -> None:
    print(f"is_palindrome({x}): {'true' if is_palindrome(x) else 'false'}")


def main() -> None:
    report(121)
    report(-121)
    report(10)
    report(0)
    report(1)
    report(11)
    report(12)
    report(12321)
    report(1221)
    report(123)
    report(1000000001)
    report(1234567899)
    report(1234554321)
    report(2147483647)
    report(-2147483648)
    report(9)
    report(99)
    report(909)
    report(900)
    report(1000021)


if __name__ == "__main__":
    main()

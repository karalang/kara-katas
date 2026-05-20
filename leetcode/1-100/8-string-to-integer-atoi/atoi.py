# LeetCode #8: String to Integer (atoi) — Python mirror of atoi.kara.
#
# Same three-phase scan (skip space, read sign, consume digits) with the
# same `INT_MAX / 10` overflow rail. Python ints are arbitrary precision,
# so we have to clamp manually — `result <= INT_MAX // 10` and the digit-8
# boundary mirror the i32-only check in the Kāra source. Returning the
# clamped sentinel directly inside the loop (rather than letting `result`
# grow past 2**31 and clamping at the end) keeps the algorithm
# structurally identical to the i32 version.

INT_MAX = 2**31 - 1   # 2_147_483_647
INT_MIN = -(2**31)    # -2_147_483_648
MAX_DIV = INT_MAX // 10   # 214_748_364

def my_atoi(s: str) -> int:
    n = len(s)
    i = 0
    while i < n and s[i] == ' ':
        i += 1

    sign = 1
    if i < n and s[i] == '+':
        i += 1
    elif i < n and s[i] == '-':
        sign = -1
        i += 1

    result = 0
    while i < n:
        c = s[i]
        if c < '0' or c > '9':
            break
        digit = ord(c) - ord('0')
        if result > MAX_DIV or (result == MAX_DIV and digit > 7):
            return INT_MAX if sign == 1 else INT_MIN
        result = result * 10 + digit
        i += 1

    return sign * result

def report(s: str) -> None:
    print(my_atoi(s))

def main() -> None:
    report("42")
    report("   -42")
    report("4193 with words")
    report("words and 987")
    report("-91283472332")
    report("91283472332")
    report("+1")
    report("")
    report("   ")
    report("+-12")
    report("-+12")
    report("  0000000000012345678")
    report("2147483647")
    report("-2147483648")
    report("2147483648")
    report("-2147483649")
    report("  +0 123")
    report("00000-42a1234")
    report("  -0012a42")
    report("+")

if __name__ == "__main__":
    main()

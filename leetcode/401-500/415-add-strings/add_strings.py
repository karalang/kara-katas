# LeetCode #415: Add Strings — reference oracle.
#
# Add two non-negative integers given as decimal strings, return the sum as a
# string. No bignum / no int() conversion — pure digit arithmetic. Identical
# column-add shape to #67 add-binary, at base 10 instead of base 2:
#
#   sum   = carry + (a[i] - '0') + (b[j] - '0')
#   digit = sum % 10
#   carry = sum // 10
#
# The lexer's base-10 `from_str_radix` arm (the decimal int-literal path),
# plus a digit-table render `"0123456789"[d]` — the inverse nibble map of
# digit parsing.

DIGITS = "0123456789"


def add_strings(a, b):
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry > 0:
        s = carry
        if i >= 0:
            s += ord(a[i]) - ord("0")
            i -= 1
        if j >= 0:
            s += ord(b[j]) - ord("0")
            j -= 1
        out.append(DIGITS[s % 10])
        carry = s // 10
    return "".join(reversed(out))


def report(a, b):
    print(f'"{a}" + "{b}" -> "{add_strings(a, b)}"')


def main():
    # LeetCode canonical examples.
    report("11", "123")            # 134
    report("456", "77")            # 533
    report("0", "0")               # 0

    # Carry ripples / new most-significant digit.
    report("9", "1")               # 10
    report("99", "1")              # 100
    report("999", "999")           # 1998
    report("1", "999999999")       # 1000000000

    # Unequal lengths.
    report("1", "9999")            # 10000
    report("12345", "54321")       # 66666
    report("100", "23")            # 123

    # Zeros and leading-digit edges.
    report("0", "12345")           # 12345
    report("500", "500")           # 1000

    # Long operands (beyond any native int width — the no-bignum point).
    report("9999999999999999999999999999999999999999", "1")  # 1 followed by forty 0s
    report("12345678901234567890", "98765432109876543210")   # 111111111011111111100


main()

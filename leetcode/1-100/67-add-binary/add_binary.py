# LeetCode #67: Add Binary — reference oracle.
#
# Add two binary strings, return the sum as a binary string. Two pointers walk
# both inputs from the least-significant end; at each step the column sum is
# `carry + digit_a + digit_b`, the emitted bit is `sum % 2`, and the next carry
# is `sum // 2`. Bits are produced least-significant first, so the buffer is
# reversed at the end.
#
# The closest corpus analog to the lexer's radix arm: `b - b'0'` digit-value
# extraction and base-N carry arithmetic, the exact shape `from_str_radix`
# walks for `0b…` literals — here base 2.


def add_binary(a, b):
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
        out.append(chr(ord("0") + (s % 2)))
        carry = s // 2
    return "".join(reversed(out))


def report(a, b):
    print(f'"{a}" + "{b}" -> "{add_binary(a, b)}"')


def main():
    # LeetCode canonical examples.
    report("11", "1")              # 100
    report("1010", "1011")         # 10101

    # Carry ripples the whole width.
    report("1", "1")               # 10
    report("111", "1")             # 1000
    report("1111", "1111")         # 11110

    # Unequal lengths, no carry past the shorter operand.
    report("100", "110010")        # 110110
    report("1", "111")             # 1000

    # Zeros.
    report("0", "0")               # 0
    report("0", "10101")           # 10101
    report("1101", "0")            # 1101

    # Longer mixed widths.
    report("10100000100100110110010000010101111011011001101110111111111101000000101111001110001111100001101", "110101001011101110001111100110001010111011010000100110101111100110001000111001000101111101110001100001110000000001")


main()

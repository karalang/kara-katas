# LeetCode #405: Convert a Number to Hexadecimal — reference oracle.
#
# Render a 32-bit integer as lowercase hex. Negatives use the 32-bit two's
# complement bit pattern (no sign, no leading zeros except "0" itself). No
# library hex conversion — pure nibble extraction:
#
#   n      = num & 0xffffffff          32-bit two's-complement, read unsigned
#   nibble = n & 0xf                   low 4 bits
#   glyph  = "0123456789abcdef"[nibble]
#   n    >>= 4                          next nibble
#
# This is the radix-16 *render* — the inverse of `from_str_radix` (the lexer's
# `0x...` hex-literal arm). The same value -> glyph nibble map digit *parsing*
# runs backwards.

HEX = "0123456789abcdef"


def to_hex(num):
    if num == 0:
        return "0"
    n = num & 0xFFFFFFFF  # 32-bit two's-complement, read as unsigned
    out = []
    while n > 0:
        out.append(HEX[n & 0xF])
        n >>= 4
    return "".join(reversed(out))


def report(num):
    print(f"{num} -> \"{to_hex(num)}\"")


def main():
    # LeetCode canonical examples.
    report(26)              # 1a
    report(0)               # 0
    report(-1)              # ffffffff

    # Power-of-16 boundaries / single nibble.
    report(1)               # 1
    report(15)              # f
    report(16)              # 10
    report(255)             # ff
    report(256)             # 100

    # 32-bit signed extremes — two's complement.
    report(2147483647)      # 7fffffff   (INT_MAX)
    report(-2147483648)     # 80000000   (INT_MIN)
    report(-26)             # ffffffe6
    report(-256)            # ffffff00


main()

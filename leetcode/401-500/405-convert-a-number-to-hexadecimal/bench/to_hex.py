# LeetCode #405 bench harness — Python peer (CPython, single-thread).
#
# Bitwise mask-and-shift hex render — same canonical algorithm as the Kara
# mirror. Sequential string-building bench: concatenate TOTAL hex renderings
# into one buffer, then byte-checksum it. Slowest lane; bounds the interpreter
# cost. Sink = byte-sum of the concatenated output.

TOTAL = 4000000
HEX = "0123456789abcdef"


def to_hex(num):
    n = num & 0xFFFFFFFF
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(HEX[n & 0xF])
        n >>= 4
    return "".join(reversed(digits))


def main():
    parts = []
    for k in range(TOTAL):
        v = (k * 2654435761) & 0xFFFFFFFF
        parts.append(to_hex(v))
    out = "".join(parts)
    print(sum(ord(c) for c in out))


main()

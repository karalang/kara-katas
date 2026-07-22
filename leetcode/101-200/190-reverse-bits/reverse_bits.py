"""LeetCode 190 — Reverse Bits (Python mirror / oracle).

Shift the answer left while peeling the input's low bit, 32 times. Mirrors the
Kāra version.
"""


def reverse_bits(n):
    result = 0
    x = n
    for _ in range(32):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result


def report(n):
    print(reverse_bits(n))


def main():
    report(43261596)
    report(4294967293)
    report(0)
    report(1)
    report(2147483648)
    report(4294967295)


main()

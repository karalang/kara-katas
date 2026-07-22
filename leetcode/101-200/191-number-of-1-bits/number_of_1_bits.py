"""LeetCode 191 — Number of 1 Bits (Python mirror / oracle).

Brian Kernighan: x & (x-1) clears the lowest set bit; loop once per set bit.
Mirrors the Kāra version.
"""


def hamming_weight(n):
    count = 0
    x = n
    while x != 0:
        x = x & (x - 1)
        count += 1
    return count


def report(n):
    print(hamming_weight(n))


def main():
    report(11)
    report(128)
    report(4294967293)
    report(0)
    report(1)
    report(4294967295)
    report(2147483648)


main()

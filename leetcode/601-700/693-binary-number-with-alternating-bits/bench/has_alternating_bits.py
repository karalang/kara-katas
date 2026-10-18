# LeetCode #693: Binary Number with Alternating Bits -- bench program, Python mirror of the ★ arm.


def has_alternating_bits(n):
    x = n ^ (n >> 1)
    return x & (x + 1) == 0


def main():
    seed = 693
    count = 100000000
    yes = 0
    checksum = 0
    for _ in range(count):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = (1431655765 >> (seed % 31)) ^ ((seed >> 8) % 4)
        if n > 0 and has_alternating_bits(n):
            yes += 1
            checksum = (checksum * 31 + n) % 1000000007
    print(f"{count} numbers: {yes} alternate, checksum {checksum}")


main()

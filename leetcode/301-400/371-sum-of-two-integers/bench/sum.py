# Benchmark for #371 -- mirror of sum.kara, with a 64-bit mask standing in
# for the i64.

MASK = (1 << 64) - 1


def get_sum(a, b):
    x = a & MASK
    carry = b & MASK
    while carry != 0:
        both = x & carry
        x = x ^ carry
        carry = (both << 1) & MASK
    return x - (1 << 64) if x >> 63 else x


def main():
    seed = 371
    checksum = 0
    for _ in range(5000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 65536) % 2001 - 1000
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 65536) % 2001 - 1000
        checksum = (checksum * 31 + get_sum(a, b) + 5000) % 1000000007
    print(f"checksum {checksum}")


main()

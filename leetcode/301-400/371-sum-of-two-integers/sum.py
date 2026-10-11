# LeetCode #371: Sum of Two Integers -- mirror of sum.kara. Python integers
# are unbounded, so the mirror keeps 64 bits with a mask and reads bit 63
# as the sign at the end, as an i64 does.

MASK = (1 << 64) - 1


def get_sum(a, b):
    x = a & MASK
    carry = b & MASK
    while carry != 0:
        both = x & carry
        x = x ^ carry
        carry = (both << 1) & MASK
    return x - (1 << 64) if x >> 63 else x


def show(label, a, b):
    print(f"{label}: {get_sum(a, b)}")


def main():
    show("example 1", 1, 2)
    show("example 2", 2, 3)
    show("zeros", 0, 0)
    show("minus one plus one", -1, 1)
    show("both at the lower bound", -1000, -1000)
    show("both at the upper bound", 1000, 1000)
    show("opposite bounds", 1000, -1000)
    show("a negative result", -7, 3)
    show("a carry through every bit", -1, -1)
    show("zero and a negative", 0, -1000)
    seed = 371
    checksum = 0
    for _ in range(5000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 65536) % 2001 - 1000
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 65536) % 2001 - 1000
        checksum = (checksum * 31 + get_sum(a, b) + 5000) % 1000000007
    print(f"5000 random pairs: checksum {checksum}")


main()

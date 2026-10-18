# LeetCode #693: Binary Number with Alternating Bits -- shift and xor.
#
# A mirror of has_alternating_bits.kara (the ★ arm) and its harness.


def has_alternating_bits(n):
    x = n ^ (n >> 1)
    return x & (x + 1) == 0


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(v):
    return "true" if v else "false"


def main():
    global seed
    h = has_alternating_bits
    print(f"5: {b(h(5))}, 7: {b(h(7))}, 11: {b(h(11))}")
    print(f"1: {b(h(1))}, 2: {b(h(2))}, 3: {b(h(3))}, 4: {b(h(4))}")
    print(f"2147483647: {b(h(2147483647))}, 1431655765: {b(h(1431655765))}, 715827882: {b(h(715827882))}")
    found = 0
    total = 0
    for n in range(1, 1000001):
        if h(n):
            found += 1
            total += n
    print(f"1 to 1000000: {found} alternate, summing to {total}")
    kept = sum(1 for k in range(31) if h(1431655765 ^ (1 << k)))
    print(f"1431655765 with one bit flipped: {kept} of 31 still alternate")
    seed = 693
    yes = 0
    checksum = 0
    for i in range(1000000):
        n = next_random() * 65536 + next_random()
        if i % 2 == 0:
            keep = next_random() % 8
            n = (1431655765 >> (next_random() % 30)) ^ (n % (1 << keep))
        if n == 0:
            n = 1
        if h(n):
            yes += 1
            checksum = (checksum * 31 + n) % 1000000007
    print(f"a million random numbers: {yes} alternate, checksum {checksum}")


main()

# LeetCode #1758: Minimum Changes To Make Alternating Binary String -- the
# ★ arm in Python, with the same harness.
def min_operations(s):
    differ = sum(1 for i, c in enumerate(s) if int(c) != i % 2)
    return min(differ, len(s) - differ)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_bits(n, ones):
    return "".join("1" if next_random() % 100 < ones else "0" for _ in range(n))


def main():
    global seed
    print(f"{min_operations('0100')} {min_operations('10')} {min_operations('1111')}")
    print(" ".join(str(min_operations(s)) for s in ["0", "1", "00", "0101010", "101010", "000000000", "1111111111"]))
    seed = 1758
    ones = "1" * 10000
    alternating = "10" * 5000
    sparse = random_bits(10000, 5)
    mixed = random_bits(10000, 50)
    print(f"10000 characters: {min_operations(ones)} {min_operations(alternating)} {min_operations(sparse)} {min_operations(mixed)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        chance = next_random() % 101
        s = random_bits(n, chance)
        check = (check * 31 + min_operations(s)) % 1000000007
    print(f"3000 random strings: checksum {check}")


main()

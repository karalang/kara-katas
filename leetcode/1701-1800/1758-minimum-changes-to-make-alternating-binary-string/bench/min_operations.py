# LeetCode #1758: Minimum Changes To Make Alternating Binary String -- the
# bench in Python, mirroring min_operations.kara: one pass counting the
# characters that differ from "0101...".
def min_operations(s):
    differ = 0
    for i, b in enumerate(s.encode()):
        if b - 48 != i % 2:
            differ += 1
    return min(differ, len(s) - differ)


def main():
    seed = 1758
    strings = []
    for _ in range(2000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + seed // 65536 % 20000
        seed = (seed * 1103515245 + 12345) % 2147483648
        chance = seed // 65536 % 101
        chars = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            chars.append("1" if seed // 65536 % 100 < chance else "0")
        strings.append("".join(chars))
    check = 0
    for call in range(30000):
        s = strings[(check + call * 7919) % 2000]
        check = (check * 31 + min_operations(s)) % 1000000007
    print(f"30000 calls over 2000 strings: checksum {check}")


main()

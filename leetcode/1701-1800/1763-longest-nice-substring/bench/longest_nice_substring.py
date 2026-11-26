# LeetCode #1763: Longest Nice Substring -- the bench in Python, mirroring
# longest_nice_substring.kara: divide and conquer at each letter whose
# other case is missing.
def longest_nice_substring(s):
    for i, c in enumerate(s):
        if c.swapcase() not in s:
            left = longest_nice_substring(s[:i])
            right = longest_nice_substring(s[i + 1:])
            return right if len(right) > len(left) else left
    return s


def main():
    seed = 1763
    strings = []
    for _ in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        letters = 1 + seed // 65536 % 12
        seed = (seed * 1103515245 + 12345) % 2147483648
        upper = seed // 65536 % 101
        chars = []
        for _ in range(100):
            seed = (seed * 1103515245 + 12345) % 2147483648
            base = 65 if seed // 65536 % 100 < upper else 97
            seed = (seed * 1103515245 + 12345) % 2147483648
            chars.append(chr(base + seed // 65536 % letters))
        strings.append("".join(chars))
    check = 0
    for call in range(500000):
        s = strings[(check + call * 7919) % 1000]
        check = (check * 31 + len(longest_nice_substring(s))) % 1000000007
    print(f"500000 calls over 1000 strings: checksum {check}")


main()

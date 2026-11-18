# LeetCode #1624: Largest Substring Between Two Equal Characters -- the
# bench in Python, mirroring gap.kara: one pass, the first index of each
# letter, and at every later sight the gap back to it.

seed = 1624


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def max_length_between_equal_characters(s):
    first = [-1] * 26
    best = -1
    for i, c in enumerate(s):
        letter = ord(c) - 97
        if first[letter] == -1:
            first[letter] = i
        else:
            best = max(best, i - first[letter] - 1)
    return best


def main():
    strings = []
    for _ in range(100000):
        n = next_random() % 300 + 1
        strings.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
    check = 0
    total = 0
    for s in strings:
        got = max_length_between_equal_characters(s)
        total += got
        check = (check * 31 + got + 1) % 1000000007
    print(f"100000 random strings: answers sum to {total}, checksum {check}")


main()

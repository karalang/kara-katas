# LeetCode #2405: Optimal Partition of String -- the Python mirror of the
# ★ arm: greedy, the current part's letters as bits of a mask.

seed = 2405


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n, kinds):
    return "".join(chr(97 + next_random() % kinds) for _ in range(n))


def partition_string(s):
    parts = 1
    seen = 0
    for ch in s:
        bit = 1 << (ord(ch) - 97)
        if seen & bit:
            parts += 1
            seen = 0
        seen |= bit
    return parts


def main():
    print(partition_string("abacaba"))
    print(partition_string("ssssss"))
    print(partition_string("a"))
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    print(f"{partition_string(alphabet)} {partition_string(alphabet * 2)}")
    print(partition_string(letters(100000, 26)))
    print(partition_string(letters(100000, 3)))
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        kinds = 1 + next_random() % 26
        a = partition_string(letters(n, kinds))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()

# LeetCode #2405: Optimal Partition of String -- the bench, the ★ arm in
# Python: greedy with a bitmask, a letter already in the current part
# starting the next one.

seed = 2405


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def partition_string(s):
    parts = 1
    seen = 0
    for b in s:
        bit = 1 << (b - 97)
        if seen & bit:
            parts += 1
            seen = 0
        seen |= bit
    return parts


def main():
    strings = [bytes(97 + next_random() % (i + 1) for _ in range(100000)) for i in range(26)]
    check = 0
    for p in range(50):
        for s in strings:
            check = (check * 31 + partition_string(s) + p) % 1000000007
    print(f"50 passes over 26 strings of 10^5 letters: checksum {check}")


main()

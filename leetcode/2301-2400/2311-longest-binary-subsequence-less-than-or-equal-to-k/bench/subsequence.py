# LeetCode #2311: Longest Binary Subsequence Less Than or Equal to K --
# the bench, the ★ arm in Python. Greedy from the right: every 0 taken,
# and a 1 taken when its place still leaves the value at most k.

seed = 2311


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_subsequence(s, k):
    value = 0
    taken = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == "0":
            taken += 1
        elif taken < 31 and value + (1 << taken) <= k:
            value += 1 << taken
            taken += 1
    return taken


def main():
    strings = []
    for _ in range(1000):
        odds = next_random() % 8 + 1
        strings.append("".join("1" if next_random() % odds == 0 else "0" for _ in range(1000)))
    check = 0
    for p in range(100):
        for a in range(1000):
            check = (check * 31 + longest_subsequence(strings[a], 10000000 * (p + 1) + a)) % 1000000007
    print(f"100 passes over 1000 strings of 1000 bits: checksum {check}")


main()

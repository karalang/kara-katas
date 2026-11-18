# LeetCode #2311: Longest Binary Subsequence Less Than or Equal to K --
# the ★ arm in Python. Greedy from the right: every 0 can be taken, and a
# 1 is taken when its place, the count of bits taken to its right, still
# leaves the value at most k.


def longest_subsequence(s, k):
    value = 0
    taken = 0
    for ch in reversed(s):
        if ch == "0":
            taken += 1
        elif taken < 31 and value + (1 << taken) <= k:
            value += 1 << taken
            taken += 1
    return taken


seed = 2311


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def bits(n, odds):
    return "".join("1" if next_random() % odds == 0 else "0" for _ in range(n))


def main():
    cases = [("1001010", 5), ("00101001", 1), ("1111", 1), ("0000", 1), ("1", 1), ("110", 6), ("1" * 36, 1000000000)]
    for s, k in cases:
        print(f"{s}, {k}: {longest_subsequence(s, k)}")
    print(f"1000 bits: {longest_subsequence(bits(1000, 2), 1000000000)}")
    check = 0
    total = 0
    for _ in range(1000):
        n = next_random() % 40 + 1
        odds = next_random() % 4 + 1
        s = bits(n, odds)
        hi = next_random()
        lo = next_random()
        k = (hi * 32768 + lo) % (1 << (next_random() % 30 + 1)) + 1
        length = longest_subsequence(s, k)
        check = (check * 31 + length) % 1000000007
        total += length
    print(f"1000 strings: checksum {check}, {total} bits in all")


main()

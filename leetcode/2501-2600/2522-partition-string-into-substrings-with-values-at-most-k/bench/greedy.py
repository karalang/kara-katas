# LeetCode #2522: Partition String Into Substrings With Values at Most K --
# benchmark mirror of the ★ arm (greedy.kara): 20 strings of 10^5 digits
# built once, then the passes, each asking every string with a k the
# checksum picks.


def minimum_partition(s, k):
    parts = 1
    value = 0
    for b in s.encode():
        d = b - 48
        if d > k:
            return -1
        value = value * 10 + d
        if value > k:
            parts += 1
            value = d
    return parts


seed = 2522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = ["".join(chr(next_random() % 9 + 1 + 48) for _ in range(100000)) for _ in range(20)]
    passes = 50
    check = 0
    for p in range(passes):
        for s in strings:
            check = (check * 31 + minimum_partition(s, check % 999999992 + 9) + p) % 1000000007
    print(f"{passes} passes over 20 strings of 10^5 digits: checksum {check}")


main()

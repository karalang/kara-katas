# LeetCode #2083: Substrings That Begin and End With the Same Letter --
# Python mirror of the ★ arm (same.kara): each letter's count c gives
# c(c + 1) / 2 substrings.


def number_of_substrings(s):
    counts = [0] * 26
    for b in s.encode():
        counts[b - ord("a")] += 1
    return sum(c * (c + 1) // 2 for c in counts)


seed = 2083


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = ["abcba", "abacad", "a", "aaaa", "abcdefghijklmnopqrstuvwxyz", "zzazz", "mississippi"]
    for s in examples:
        print(f"{s} -> {number_of_substrings(s)}")
    letters = "abcdefghijklmnopqrstuvwxyz"
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 200 + 1
        width = [1, 2, 5, 26][next_random() % 4]
        s = "".join(letters[next_random() % width] for _ in range(n))
        a = number_of_substrings(s)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2000 strings: sum {total}, checksum {check}")
    s = "".join(letters[next_random() % 3] for _ in range(100000))
    print(f"100000 letters: {number_of_substrings(s)}")


main()

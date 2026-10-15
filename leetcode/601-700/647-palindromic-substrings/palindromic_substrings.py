# LeetCode #647: Palindromic Substrings -- expanding from each center.
# Mirrors the ★ arm (palindromic_substrings.kara) and its test harness.


def count_substrings(s):
    n = len(s)
    count = 0
    for center in range(2 * n - 1):
        lo = center // 2
        hi = lo + center % 2
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            count += 1
            lo -= 1
            hi += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}" -> {count_substrings(s)}')


def random_text(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    global seed
    for s in ["abc", "aaa", "z", "ab", "bb", "racecar", "abba", "xabbay",
              "aaaabaaaa", "abababa", "abacdfgdcaba"]:
        show(s)
    seed = 647
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 40
        letters = 1 + next_random() % 4
        c = count_substrings(random_text(n, letters))
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    print(f"1000 of one letter: {count_substrings(random_text(1000, 1))}")
    print(f"1000 of two letters: {count_substrings(random_text(1000, 2))}")
    print(f"1000 of 26 letters: {count_substrings(random_text(1000, 26))}")


main()

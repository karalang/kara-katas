# LeetCode #1456 Maximum Number of Vowels in a Substring of Given Length: a
# mirror of max_vowels.kara.


def max_vowels(s, k):
    # a window of k letters slid along the string, its vowels counted as a
    # letter comes in and another goes out
    def is_vowel(c):
        return c in "aeiou"
    count = sum(1 for c in s[:k] if is_vowel(c))
    best = count
    for i in range(k, len(s)):
        if is_vowel(s[i]):
            count += 1
        if is_vowel(s[i - k]):
            count -= 1
        best = max(best, count)
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text(n, odds):
    vowels = "aeiou"
    others = "bcdfghjklmnpqrstvwxyz"
    out = []
    for _ in range(n):
        if next_random() % odds == 0:
            out.append(vowels[next_random() % 5])
        else:
            out.append(others[next_random() % 21])
    return "".join(out)


def main():
    global seed
    cases = [("abciiidef", 3), ("aeiou", 2), ("leetcode", 3), ("a", 1), ("rhythm", 4), ("education", 9)]
    for s, k in cases:
        print(max_vowels(s, k))
    seed = 1456
    long = text(100000, 3)
    print(f"10^5 letters: {max_vowels(long, 1)} {max_vowels(long, 1000)} {max_vowels(long, 100000)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        odds = 1 + next_random() % 5
        k = 1 + next_random() % n
        got = max_vowels(text(n, odds), k)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} vowels, checksum {check}")


main()

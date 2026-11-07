# LeetCode #1062: Longest Repeating Substring -- the Python mirror of
# lrs.kara (the ★ arm): a binary search on the length, each step a rolling
# hash over the substrings of that length, each match checked byte for byte.

MOD = 1000000007
BASE = 131


def twice(s, length):
    if length == 0:
        return True
    top = 1
    for _ in range(1, length):
        top = top * BASE % MOD
    h = 0
    seen = {}
    for i in range(len(s)):
        if i >= length:
            h = (h - s[i - length] * top % MOD + MOD) % MOD
        h = (h * BASE + s[i]) % MOD
        if i + 1 >= length:
            start = i + 1 - length
            starts = seen.setdefault(h, [])
            for other in starts:
                if s[other:other + length] == s[start:start + length]:
                    return True
            starts.append(start)
    return False


def longest_repeating(s):
    b = s.encode()
    lo, hi = 0, len(b)
    while hi - lo > 1:
        mid = lo + (hi - lo) // 2
        if twice(b, mid):
            lo = mid
        else:
            hi = mid
    return lo


# ---- test harness ---------------------------------------------------------

seed = 1062


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def main():
    for s in ["abcd", "abbaba", "aabcaabdaab", "aaaaa", "a", "ab", "aa", "abab", "abcabcabc", "mississippi"]:
        print(f"{s} -> {longest_repeating(s)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        k = next_random() % 3 + 1
        answer = longest_repeating(random_word(n, k))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"3000 strings of 1 to 12 letters over 1 to 3: sum {total}, checksum {check}")
    total = check = 0
    for i in range(300):
        n = next_random() % 251 + 50
        answer = longest_repeating(random_word(n, 2 + i % 25))
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"300 strings of 50 to 300 letters over 2 to 26: sum {total}, checksum {check}")
    for k in [2, 4, 26]:
        print(f"2000 letters over {k}: {longest_repeating(random_word(2000, k))}")
    a, b = "a", "ab"
    while len(b) < 2000:
        a, b = b, b + a
    print(f"Fibonacci word of 2000: {longest_repeating(b[:2000])}")
    print(f"2000 z's: {longest_repeating('z' * 2000)}")


main()

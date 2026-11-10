# LeetCode #1092: Shortest Common Supersequence -- Python mirror of the ★
# arm: the longest-common-subsequence table, walked back from the full
# words, a shared last letter written once and otherwise the letter the LCS
# does not need given up first.


def shortest_common_supersequence(a, b):
    n, m = len(a), len(b)
    lcs = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
            else:
                lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
    out = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif lcs[i - 1][j] >= lcs[i][j - 1]:
            out.append(a[i - 1])
            i -= 1
        else:
            out.append(b[j - 1])
            j -= 1
    while i > 0:
        out.append(a[i - 1])
        i -= 1
    while j > 0:
        out.append(b[j - 1])
        j -= 1
    return "".join(reversed(out))


seed = 1092


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def is_subsequence(a, s):
    it = iter(s)
    return all(any(d == c for d in it) for c in a)


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def judge(a, b):
    s = shortest_common_supersequence(a, b)
    ok = "both in it" if is_subsequence(a, s) and is_subsequence(b, s) else "MISSING ONE"
    return f"{len(s)}, {ok}"


def main():
    cases = [
        ("abac", "cab"),
        ("aaaaaaaa", "aaaaaaaa"),
        ("a", "b"),
        ("abc", "abc"),
        ("abc", "def"),
        ("abcde", "ace"),
        ("ace", "abcde"),
        ("geek", "eke"),
        ("aggtab", "gxtxayb"),
        ("bbbaaaba", "bbababbb"),
        ("leetcode", "codeleet"),
        ("z", "zzzzz"),
    ]
    for a, b in cases:
        print(f"{a} {b} -> {judge(a, b)}")
    total = bad = h = 0
    for _ in range(2000):
        a = random_word(next_random() % 12 + 1, 3)
        b = random_word(next_random() % 12 + 1, 3)
        s = shortest_common_supersequence(a, b)
        if not (is_subsequence(a, s) and is_subsequence(b, s)):
            bad += 1
        total += len(s)
        h = (h * 31 + len(s)) % 1000000007
    print(f"2000 random pairs: lengths sum to {total}, {bad} missing a word, checksum {h}")
    for letters in (26, 4):
        a = random_word(1000, letters)
        b = random_word(1000, letters)
        print(f"1000 and 1000 letters from {letters}: {judge(a, b)}")


main()

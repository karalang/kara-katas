# LeetCode #727: Minimum Window Subsequence -- forward, then back.
# Mirror of the Kara star arm and its harness.


def min_window(s1, s2):
    n, m = len(s1), len(s2)
    best_start, best_len = -1, n + 1
    i = 0
    while i < n:
        j = 0
        while i < n:
            if s1[i] == s2[j]:
                j += 1
                if j == m:
                    break
            i += 1
        if j < m:
            break
        end = i
        k = m - 1
        p = end
        while k >= 0:
            if s1[p] == s2[k]:
                k -= 1
            p -= 1
        start = p + 1
        if end - start + 1 < best_len:
            best_len = end - start + 1
            best_start = start
        i = start + 1
    if best_start < 0:
        return ""
    return s1[best_start:best_start + best_len]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(n, kinds, seed):
    return "".join(chr(ord("a") + next_random(seed) % kinds) for _ in range(n))


def show(s1, s2):
    print(f'"{s1}", "{s2}" -> "{min_window(s1, s2)}"')


def summary(what, s1, s2):
    w = min_window(s1, s2)
    at = s1.find(w) if w else -1
    print(f"{what} -> length {len(w)} at {at}")


def main():
    show("abcdebdde", "bde")
    show("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u")
    show("abc", "abc")
    show("ab", "abc")
    show("abab", "ab")
    show("aaaa", "aa")
    show("cnhczmccqouqadqtmjjzl", "mm")
    show("fgrqsqsnodwmxzkzxwqegkndaa", "kzed")
    show("zzzzaz", "az")
    seed = [727]
    s1 = random_word(20000, 26, seed)
    s2 = random_word(100, 26, seed)
    summary("20000 random letters, 100 random letters", s1, s2)
    s3 = random_word(20000, 3, seed)
    s4 = random_word(100, 3, seed)
    summary("20000 of 3 letters, 100 of 3 letters", s3, s4)
    summary("20000 a's, 100 a's", "a" * 20000, "a" * 100)
    summary("ab 10000 times then c, ab 50 times then c", "ab" * 10000 + "c", "ab" * 50 + "c")
    total = 0
    found = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 15
        m = 1 + next_random(seed) % 4
        kinds = 1 + next_random(seed) % 3
        w = min_window(random_word(n, kinds, seed), random_word(m, kinds, seed))
        if w:
            found += 1
        for c in w.encode():
            total = (total * 131 + c) % 1000000007
        total = (total * 131 + len(w) + 1) % 1000000007
    print(f"300 random pairs: {found} with a window, checksum {total}")


main()

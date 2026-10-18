# LeetCode #730: Count Different Palindromic Subsequences -- by interval.
# Mirror of the Kara star arm and its harness.

M = 1000000007


def count_palindromic_subsequences(s):
    n = len(s)
    next_same = [n] * n
    prev_same = [-1] * n
    last = {}
    for i, ch in enumerate(s):
        prev_same[i] = last.get(ch, -1)
        if ch in last:
            next_same[last[ch]] = i
        last[ch] = i
    count = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        count[i][i] = 1
        for j in range(i + 1, n):
            inner = count[i + 1][j - 1] if i + 1 <= j - 1 else 0
            if s[i] != s[j]:
                v = count[i + 1][j] + count[i][j - 1] - inner
            else:
                lo, hi = next_same[i], prev_same[j]
                if lo > hi:
                    v = 2 * inner + 2
                elif lo == hi:
                    v = 2 * inner + 1
                else:
                    twice = count[lo + 1][hi - 1] if lo + 1 <= hi - 1 else 0
                    v = 2 * inner - twice
            count[i][j] = v % M
    return count[0][n - 1]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(n, kinds, seed):
    return "".join(chr(ord("a") + next_random(seed) % kinds) for _ in range(n))


def show(s):
    print(f'"{s}" -> {count_palindromic_subsequences(s)}')


def main():
    show("bccb")
    show("abcdabcdabcdabcdabcdabcdabcdabcddcbadcbadcbadcbadcbadcbadcbadcba")
    show("a")
    show("aaaa")
    show("abcd")
    show("aba")
    show("abba")
    show("aabbaa")
    show("dcbabcd")
    seed = [730]
    big = random_word(1000, 4, seed)
    print(f"1000 random letters -> {count_palindromic_subsequences(big)}")
    two = random_word(1000, 2, seed)
    print(f"1000 random a's and b's -> {count_palindromic_subsequences(two)}")
    print(f"1000 a's -> {count_palindromic_subsequences('a' * 1000)}")
    print(f"abcd 250 times -> {count_palindromic_subsequences('abcd' * 250)}")
    total = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 30
        kinds = 1 + next_random(seed) % 4
        v = count_palindromic_subsequences(random_word(n, kinds, seed))
        total = (total * 131 + v) % 1000000007
    print(f"300 random strings: checksum {total}")


main()

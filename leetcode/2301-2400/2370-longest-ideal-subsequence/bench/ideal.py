# LeetCode #2370: Longest Ideal Subsequence -- the bench, the ★ arm in
# Python: best[c] is the longest ideal subsequence so far ending in letter
# c, and a new letter extends the best one within k letters of it.


def longest_ideal_string(s, k):
    best = [0] * 26
    for b in s.encode():
        c = b - 97
        lo = max(c - k, 0)
        hi = min(c + k, 25)
        most = 0
        for d in range(lo, hi + 1):
            if best[d] > most:
                most = best[d]
        best[c] = most + 1
    return max(best)


SEED = [2370]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # string a: 10^5 random letters from the whole alphabet, answered with
    # k of a and of 2 a + 5
    strings = []
    for _ in range(10):
        strings.append("".join(chr(97 + next_random() % 26) for _ in range(100000)))
    check = 0
    for p in range(10):
        for a in range(10):
            for k in (a, 2 * a + 5):
                check = (check * 31 + longest_ideal_string(strings[a], k) + p) % 1000000007
    print(f"10 passes over 10 strings of 10^5 letters: checksum {check}")


main()

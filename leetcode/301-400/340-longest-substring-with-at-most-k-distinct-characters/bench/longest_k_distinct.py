# Benchmark mirror of longest_k_distinct.kara (LeetCode #340): a sliding
# window with a count per character in a dict. Same strings, rounds and sink.

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def longest_k_distinct(s, k):
    counts = {}
    left = 0
    best = 0
    for right in range(len(s)):
        c = s[right]
        counts[c] = counts.get(c, 0) + 1
        while len(counts) > k:
            d = s[left]
            n = counts[d] - 1
            if n == 0:
                del counts[d]
            else:
                counts[d] = n
            left += 1
        best = max(best, right - left + 1)
    return best


def gen_text(seed, n, alpha):
    state = seed
    out = []
    for _ in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        out.append(LETTERS[(state >> 8) % alpha])
    return "".join(out)


def main():
    alphas = [4, 8, 12, 20, 26, 34, 44, 52]
    texts = [gen_text(1000 + i, 20000, alphas[i]) for i in range(8)]
    h = 0
    for r in range(400):
        k = (r * 7) % 30 + 1
        h = (h * 31 + longest_k_distinct(texts[r % 8], k)) % 1000000007
    print(h)


main()

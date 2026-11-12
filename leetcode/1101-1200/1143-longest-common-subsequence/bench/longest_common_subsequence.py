# LeetCode #1143: Longest Common Subsequence -- the bench in Python, the
# ★ arm's algorithm.


def longest_common_subsequence(text1, text2):
    a, b = text1, text2
    m, n = len(a), len(b)
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                best[i][j] = best[i - 1][j - 1] + 1
            else:
                best[i][j] = max(best[i - 1][j], best[i][j - 1])
    return best[m][n]


seed = 1143


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcd"
    texts = [[letters[next_random() % 4] for _ in range(1000)] for _ in range(20)]
    total = 0
    check = 0
    for _ in range(10):
        for p in range(10):
            for t in (2 * p, 2 * p + 1):
                at = next_random() % 1000
                texts[t][at] = letters[next_random() % 4]
            answer = longest_common_subsequence("".join(texts[2 * p]), "".join(texts[2 * p + 1]))
            total += answer
            check = (check * 131 + answer + 1) % 1000000007
    print(f"10 rounds over 10 pairs of 1000 letters: answers total {total}, checksum {check}")


main()

# Benchmark: LeetCode #1092 Shortest Common Supersequence -- Python mirror of
# the ★ arm: the longest common subsequence's table, a list of rows,
# walked back from the end. Same workload and sink as
# shortest_common_supersequence.kara.


def shortest_common_supersequence(a, b):
    x, y = list(a), list(b)
    n, m = len(x), len(y)
    lcs = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
            else:
                lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
    out = []
    i, j = n, m
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            out.append(x[i - 1])
            i -= 1
            j -= 1
        elif lcs[i - 1][j] >= lcs[i][j - 1]:
            out.append(x[i - 1])
            i -= 1
        else:
            out.append(y[j - 1])
            j -= 1
    while i > 0:
        out.append(x[i - 1])
        i -= 1
    while j > 0:
        out.append(y[j - 1])
        j -= 1
    return "".join(reversed(out))


seed = 1092


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    pairs = []
    for k in range(50):
        letters = 2 + k % 25
        a = random_word(1000, letters)
        b = random_word(1000, letters)
        pairs.append((a, b))
    total = check = 0
    for _ in range(4):
        for a, b in pairs:
            s = shortest_common_supersequence(a, b)
            n = len(s)
            total += n
            check = (check * 31 + n) % 1000000007
            check = (check * 31 + ord(s[n // 3])) % 1000000007
            check = (check * 31 + ord(s[2 * n // 3])) % 1000000007
    print(f"4 rounds over 50 pairs of 1000 letters: lengths sum to {total}, checksum {check}")


main()

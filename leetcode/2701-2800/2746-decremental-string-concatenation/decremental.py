# LeetCode #2746: Decremental String Concatenation -- the ★ arm in Python
# (decremental.kara): the shortest string for each pair of first and last
# letters, rolled word by word with the word put after or before.

NONE = 1000000000


def minimize_concatenated_length(words):
    best = [[NONE] * 26 for _ in range(26)]
    best[ord(words[0][0]) - 97][ord(words[0][-1]) - 97] = len(words[0])
    for w in words[1:]:
        a, b = ord(w[0]) - 97, ord(w[-1]) - 97
        nxt = [[NONE] * 26 for _ in range(26)]
        for f in range(26):
            for l in range(26):
                length = best[f][l]
                if length == NONE:
                    continue
                after = length + len(w) - (1 if l == a else 0)
                nxt[f][b] = min(nxt[f][b], after)
                before = length + len(w) - (1 if b == f else 0)
                nxt[a][l] = min(nxt[a][l], before)
        best = nxt
    return min(min(row) for row in best)


seed = 2746


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(n, longest, k):
    words = []
    for _ in range(n):
        length = next_random() % longest + 1
        words.append("".join(chr(97 + next_random() % k) for _ in range(length)))
    return words


def main():
    print(minimize_concatenated_length(["aa", "ab", "bc"]))
    print(minimize_concatenated_length(["ab", "b"]))
    print(minimize_concatenated_length(["aaa", "c", "aba"]))
    print(minimize_concatenated_length(["xyz"]))
    print(minimize_concatenated_length(["a" * 50] * 1000))
    total = check = 0
    for _ in range(3000):
        k = next_random() % 3 + 1
        n = next_random() % 12 + 1
        length = minimize_concatenated_length(random_words(n, 4, k))
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"3000 small lists: lengths sum to {total}, checksum {check}")
    total = check = 0
    for _ in range(30):
        length = minimize_concatenated_length(random_words(1000, 50, 5))
        total += length
        check = (check * 31 + length) % 1000000007
    print(f"30 lists of 1000 words: lengths sum to {total}, checksum {check}")


main()

# LeetCode #2746: Decremental String Concatenation -- the bench
# (decremental.kara in Python): the shortest string for each pair of first
# and last letters, rolled word by word.

NONE = 1000000000


def minimize_concatenated_length(words):
    best = [[NONE] * 26 for _ in range(26)]
    best[ord(words[0][0]) - 97][ord(words[0][-1]) - 97] = len(words[0])
    for w in words[1:]:
        a, b = ord(w[0]) - 97, ord(w[-1]) - 97
        n = len(w)
        nxt = [[NONE] * 26 for _ in range(26)]
        for f in range(26):
            row = best[f]
            for l in range(26):
                length = row[l]
                if length == NONE:
                    continue
                after = length + n - (1 if l == a else 0)
                if after < nxt[f][b]:
                    nxt[f][b] = after
                before = length + n - (1 if b == f else 0)
                if before < nxt[a][l]:
                    nxt[a][l] = before
        best = nxt
    return min(min(row) for row in best)


seed = 2746


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 100, 5
    lists = []
    for _ in range(count):
        words = []
        for _ in range(1000):
            n = next_random() % 10 + 1
            words.append("".join(chr(97 + next_random() % 26) for _ in range(n)))
        lists.append(words)
    total = check = 0
    for r in range(rounds):
        for words in lists:
            length = minimize_concatenated_length(words)
            total += length
            check = (check * 31 + length + r) % 1000000007
    print(f"{count} lists of 1000 words, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()

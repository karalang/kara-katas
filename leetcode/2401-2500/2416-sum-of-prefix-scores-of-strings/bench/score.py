# LeetCode #2416: Sum of Prefix Scores of Strings -- the bench, the ★ arm:
# a trie in flat arrays, node k's child by letter c at `nxt[26 k + c]` and
# `count[k]` the words through it.

seed = 2416


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sum_prefix_scores(words):
    nxt = [0] * 26
    count = [0]
    for w in words:
        at = 0
        for b in w:
            c = b - 97
            if nxt[26 * at + c] == 0:
                nxt[26 * at + c] = len(count)
                count.append(0)
                nxt.extend([0] * 26)
            at = nxt[26 * at + c]
            count[at] += 1
    scores = []
    for w in words:
        at = 0
        score = 0
        for b in w:
            at = nxt[26 * at + b - 97]
            score += count[at]
        scores.append(score)
    return scores


def main():
    lists = []
    for i in range(10):
        words = []
        for _ in range(2000):
            n = 1 + next_random() % 50
            words.append(bytes(97 + next_random() % (2 + 2 * i) for _ in range(n)))
        lists.append(words)
    check = 0
    for p in range(20):
        for words in lists:
            for s in sum_prefix_scores(words):
                check = (check * 31 + s + p) % 1000000007
    print(f"20 passes over 10 lists of 2000 words: checksum {check}")


main()

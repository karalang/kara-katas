# LeetCode #720: Longest Word in Dictionary -- a trie, walked through
# word ends only. Benchmark mirror of the Kara trie arm: every word put
# in a trie with one array of 26 children per node, then a depth-first
# walk that steps only onto nodes where a word ends.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def deepest(nxt, word_at, node, depth):
    best = (depth, word_at[node])
    for c in range(26):
        child = nxt[node][c]
        if child != 0 and word_at[child] >= 0:
            got = deepest(nxt, word_at, child, depth + 1)
            if got[0] > best[0]:
                best = got
    return best


def longest_word(words):
    nxt = [[0] * 26]
    word_at = [-1]
    for i, w in enumerate(words):
        node = 0
        for ch in w:
            c = ord(ch) - 97
            if nxt[node][c] == 0:
                nxt[node][c] = len(nxt)
                nxt.append([0] * 26)
                word_at.append(-1)
            node = nxt[node][c]
        word_at[node] = i
    found = deepest(nxt, word_at, 0, 0)
    return "" if found[1] < 0 else words[found[1]]


def main():
    seed = [720]
    dicts = []
    for _ in range(40):
        words = []
        for _ in range(1000):
            if words and next_random(seed) % 4 != 0:
                w = words[next_random(seed) % len(words)]
                if len(w) < 30:
                    w += chr(97 + next_random(seed) % 4)
                words.append(w)
            else:
                n = 1 + next_random(seed) % 3
                words.append("".join(chr(97 + next_random(seed) % 4) for _ in range(n)))
        dicts.append(words)
    total = 0
    for rnd in range(300):
        for d in range(40):
            i = (rnd * 7919 + d * 104729) % 1000
            if len(dicts[d][i]) < 30:
                dicts[d][i] += chr(97 + rnd % 4)
            total += len(longest_word(dicts[d]))
    print(f"300 rounds of 40 dictionaries of 1000 words: sum {total}")


main()

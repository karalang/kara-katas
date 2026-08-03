"""Benchmark mirror for LeetCode #244 - Shortest Word Distance II.

Same algorithm, same LCG, same sink as the Kara/C/Rust/Go mirrors: build the
20,000-word list and its position index ONCE (index-pool construction: word ->
slot, plus a side list of position lists), then punch 200,000 two-pointer merge
queries over distinct vocabulary pairs.

Timed separately from the compiled lanes - see BENCHMARKS.md.
"""

VOCAB_N = 256
N = 20000
ITERS = 200000


def lcg(state):
    return (state * 1103515245 + 12345) & 2147483647


class WordDistance:
    def __init__(self, words):
        self.slot = {}
        self.lists = []
        self.size = len(words)
        for i, w in enumerate(words):
            s = self.slot.get(w)
            if s is None:
                self.slot[w] = len(self.lists)
                self.lists.append([i])
            else:
                self.lists[s].append(i)

    def shortest(self, word1, word2):
        s1 = self.slot.get(word1)
        if s1 is None:
            return self.size
        s2 = self.slot.get(word2)
        if s2 is None:
            return self.size
        p1 = self.lists[s1]
        p2 = self.lists[s2]
        best = self.size
        a = 0
        b = 0
        while a < len(p1) and b < len(p2):
            d = p1[a] - p2[b]
            if d < 0:
                d = -d
            if d < best:
                best = d
            if p1[a] < p2[b]:
                a += 1
            else:
                b += 1
        return best


def main():
    alpha = ["a", "b", "c", "d"]
    vocab = []
    for v in range(VOCAB_N):
        vocab.append(
            "delta"
            + alpha[(v // 64) % 4]
            + alpha[(v // 16) % 4]
            + alpha[(v // 4) % 4]
            + alpha[v % 4]
        )

    state = 1
    words = []
    for _ in range(N):
        state = lcg(state)
        words.append(vocab[(state // 65536) % VOCAB_N])

    wd = WordDistance(words)

    acc = 0
    qstate = 7
    for _ in range(ITERS):
        qstate = lcg(qstate)
        a = (qstate // 65536) % VOCAB_N
        qstate = lcg(qstate)
        b = (qstate // 65536) % VOCAB_N
        if b == a:
            b = (b + 1) % VOCAB_N
        d = wd.shortest(vocab[a], vocab[b])
        acc = (acc * 131 + d) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()

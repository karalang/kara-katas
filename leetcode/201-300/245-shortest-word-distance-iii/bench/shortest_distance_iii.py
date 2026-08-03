"""Benchmark mirror for LeetCode #245 - Shortest Word Distance III.

Same algorithm, same LCG, same sink as the Kara/C/Rust/Go mirrors, and the same
workload as #243's bench so the two are directly comparable. Half the punches
are same-word queries - the case #243 cannot answer.

Timed separately from the compiled lanes - see BENCHMARKS.md.
"""

VOCAB_N = 256
N = 20000
ITERS = 2000


def lcg(state):
    return (state * 1103515245 + 12345) & 2147483647


def shortest_word_distance(words, word1, word2):
    n = len(words)
    same = word1 == word2
    best = n
    prev = -1
    for i in range(n):
        if words[i] == word1 or words[i] == word2:
            if prev != -1 and (same or words[prev] != words[i]):
                if i - prev < best:
                    best = i - prev
            prev = i
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

    acc = 0
    qstate = 7
    for k in range(ITERS):
        qstate = lcg(qstate)
        a = (qstate // 65536) % VOCAB_N
        qstate = lcg(qstate)
        b = (qstate // 65536) % VOCAB_N
        if b == a:
            b = (b + 1) % VOCAB_N
        if k % 2 == 0:
            d = shortest_word_distance(words, vocab[a], vocab[a])
        else:
            d = shortest_word_distance(words, vocab[a], vocab[b])
        acc = (acc * 131 + d) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()

"""Benchmark harness for LeetCode #243 — Shortest Word Distance.

Mirrors shortest_distance.kara algorithm-for-algorithm. This is the correctness
oracle for the sink, not a timed lane — bench-lib.sh skips it unless
KARA_BENCH_INCLUDE_PY=1. At 40M slot visits it takes seconds, not milliseconds.
"""

VOCAB_N = 256
N = 20000
ITERS = 2000


def shortest_distance(words, word1, word2):
    n = len(words)
    last1 = -1
    last2 = -1
    best = n
    for i in range(n):
        if words[i] == word1:
            last1 = i
            if last2 >= 0:
                best = min(best, last1 - last2)
        elif words[i] == word2:
            last2 = i
            if last1 >= 0:
                best = min(best, last2 - last1)
    return best


def lcg(state):
    """Overflow-free 31-bit LCG; every draw uses bits 16..23."""
    return (state * 1103515245 + 12345) & 2147483647


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

    # ''.join forces a fresh object per slot, matching the .clone()/strings.Clone
    # in the compiled mirrors — no slot aliases a vocabulary entry.
    words = []
    state = 1
    for _ in range(N):
        state = lcg(state)
        words.append("".join(vocab[(state // 65536) % VOCAB_N]))

    acc = 0
    qstate = 7
    for _ in range(ITERS):
        qstate = lcg(qstate)
        a = (qstate // 65536) % VOCAB_N
        qstate = lcg(qstate)
        b = (qstate // 65536) % VOCAB_N
        if b == a:
            b = (b + 1) % VOCAB_N
        d = shortest_distance(words, vocab[a], vocab[b])
        acc = (acc * 131 + d) % 1000000007
    print(acc)


if __name__ == "__main__":
    main()

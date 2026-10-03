# Benchmark workload for LeetCode #336 — Python mirror of
# palindrome_pairs.kara (same words, same punches, same sink).

WORDS = 20000
PUNCHES = 50
MODULUS = 1073741789


def is_palindrome(b, lo, hi):
    i, j = lo, hi - 1
    while i < j:
        if b[i] != b[j]:
            return False
        i += 1
        j -= 1
    return True


def palindrome_pairs(words):
    index = {w[::-1]: i for i, w in enumerate(words)}
    pairs = []
    for i, w in enumerate(words):
        n = len(w)
        for k in range(n + 1):
            if is_palindrome(w, k, n):
                j = index.get(w[:k])
                if j is not None and j != i:
                    pairs.append((i, j))
            if k > 0 and is_palindrome(w, 0, k):
                j = index.get(w[k:])
                if j is not None and j != i:
                    pairs.append((j, i))
    pairs.sort()
    return pairs


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    alphabet = "abc"
    rng = Rng(336)
    seen = set()
    words = []
    while len(words) < WORDS:
        n = 1 + rng.next() % 10
        w = "".join(alphabet[rng.next() % 3] for _ in range(n))
        if w not in seen:
            seen.add(w)
            words.append(w)
    sink = 0
    for _ in range(PUNCHES):
        at = rng.next() % WORDS
        old = words[at]
        words[at] = old + "d"
        pairs = palindrome_pairs(words)
        words[at] = old
        sink = (sink * 1000003 + len(pairs)) % MODULUS
        for i, j in pairs:
            sink = (sink * 31 + i * 7 + j) % MODULUS
    print(sink)


main()

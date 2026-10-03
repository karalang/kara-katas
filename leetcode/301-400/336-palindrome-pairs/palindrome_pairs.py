# LeetCode #336: Palindrome Pairs — a map of reversed words.
# Python mirror of palindrome_pairs.kara; prints the same lines.


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


def random_words(rng, count, letters, lo, hi):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    seen = set()
    out = []
    while len(out) < count:
        n = lo + rng.next() % (hi - lo + 1)
        w = "".join(alphabet[rng.next() % letters] for _ in range(n))
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


def show(words):
    pairs = palindrome_pairs(words)
    shown = ", ".join(f'"{w}"' for w in words)
    found = " ".join(f"({i}, {j})" for i, j in pairs)
    print(f"[{shown}] -> {found}")


def main():
    show(["abcd", "dcba", "lls", "s", "sssll"])
    show(["bat", "tab", "cat"])
    show(["a", ""])
    show([])
    show([""])
    show(["a", "b", "c"])
    show(["", "a", "aa", "aba"])
    show(["abc", "cba", "ab", "ba"])
    show(["race", "car", "ecar"])
    show(["ab", "a", "ba", "b"])
    show(["aab", "baa", "aaa", "b"])
    show(["xyzzyx", "xyz", "zyx", "zzyx"])
    rng = Rng(336)
    for rnd in range(6):
        show(random_words(rng, 4 + rnd, 2 + rnd % 2, 0, 4))
    big = random_words(rng, 1000, 2, 1, 12)
    pairs = palindrome_pairs(big)
    h = 0
    for i, j in pairs:
        h = (h * 1000003 + i * 4099 + j) % 1073741789
    print(f"big: {len(big)} words -> {len(pairs)} pairs, hash {h}")


main()

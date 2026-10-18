# LeetCode 745 — Prefix and Suffix Search, every pair in a map.
# Mirror of prefix_and_suffix_search.kara (the ★ arm); same output, byte for byte.


class WordFilter:
    def __init__(self, words):
        self.keys = {}
        for i, w in enumerate(words):
            n = len(w)
            for p in range(n + 1):
                for s in range(n + 1):
                    self.keys[w[:p] + "{" + w[s:]] = i

    def f(self, pref, suff):
        return self.keys.get(pref + "{" + suff, -1)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(text, queries):
    flt = WordFilter(text.split(" "))
    line = "[" + text + "]:"
    for pref, suff in queries:
        line += f" f({pref}, {suff}) = {flt.f(pref, suff)}"
    print(line)


def random_word(rng, longest, letters):
    n = 1 + rng.next() % longest
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def main():
    show("apple", [("a", "e")])
    show("apple apply ape pale", [("a", "e"), ("ap", "y"), ("p", "e"), ("apple", "apple"), ("b", "e")])
    show("abc abc", [("a", "c"), ("abc", "abc")])
    show("a ab ba", [("a", "a"), ("ab", "ab"), ("aba", "a"), ("b", "a")])
    show("abcdefg gfedcba", [("abcdefg", "g"), ("g", "gfedcba"), ("abc", "cba")])

    rng = Rng(745)
    words = [random_word(rng, 7, 5) for _ in range(10000)]
    flt = WordFilter(words)
    found = 0
    total = 0
    for _ in range(3000):
        pref = random_word(rng, 4, 5)
        suff = random_word(rng, 4, 5)
        got = flt.f(pref, suff)
        if got != -1:
            found += 1
            total += got
    print(f"10000 words of up to 7 letters from a to e, 3000 queries: {found} found, indices sum to {total}")

    hits = 0
    check = 0
    for _ in range(300):
        n = 1 + rng.next() % 10
        small = [random_word(rng, 4, 3) for _ in range(n)]
        flt = WordFilter(small)
        for _ in range(10):
            pref = random_word(rng, 3, 3)
            suff = random_word(rng, 3, 3)
            got = flt.f(pref, suff)
            if got != -1:
                hits += 1
            check = (check * 31 + got + 2) % 1000000007
    print(f"300 random filters, 3000 queries: {hits} found, checksum {check}")


main()

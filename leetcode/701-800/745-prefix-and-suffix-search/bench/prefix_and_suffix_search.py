# LeetCode 745 — Prefix and Suffix Search, bench: the ★ arm (every
# prefix-suffix pair of every word in a map) on filters of 10000
# words, each asked 10000 queries. Mirrors prefix_and_suffix_search.kara.


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


seed = 745


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest, letters):
    n = 1 + next_random() % longest
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    rounds = 5
    found = 0
    total = 0
    for _ in range(rounds):
        words = [random_word(7, 5) for _ in range(10000)]
        flt = WordFilter(words)
        for _ in range(10000):
            pref = random_word(4, 5)
            suff = random_word(4, 5)
            got = flt.f(pref, suff)
            if got != -1:
                found += 1
                total += got
    print(f"{rounds} rounds of 10000 words and 10000 queries: {found} found, indices sum to {total}")


main()

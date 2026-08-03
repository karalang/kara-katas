"""LeetCode 244 - Shortest Word Distance II (reference oracle).

Same shape as the Kara version: build word -> ascending positions once at
construction, then answer each query by a two-pointer merge over the two lists.
`best` starts at the list length, the same upper bound the Kara version uses, so
the "word absent" case agrees too.
"""


class WordDistance:
    def __init__(self, words):
        self.index = {}
        self.size = len(words)
        for i, w in enumerate(words):
            self.index.setdefault(w, []).append(i)

    def shortest(self, word1, word2):
        p1 = self.index.get(word1, [])
        p2 = self.index.get(word2, [])
        best = self.size
        a = 0
        b = 0
        while a < len(p1) and b < len(p2):
            best = min(best, abs(p1[a] - p2[b]))
            if p1[a] < p2[b]:
                a += 1
            else:
                b += 1
        return best


def report(wd, word1, word2):
    print(f"{word1} <-> {word2} : {wd.shortest(word1, word2)}")


def main():
    d1 = ["practice", "makes", "perfect", "coding", "makes"]
    wd1 = WordDistance(d1)
    report(wd1, "coding", "practice")
    report(wd1, "makes", "coding")
    report(wd1, "makes", "perfect")
    report(wd1, "practice", "perfect")

    d2 = ["a", "b", "x", "x", "x", "a", "b"]
    wd2 = WordDistance(d2)
    report(wd2, "a", "b")
    report(wd2, "b", "a")
    report(wd2, "a", "x")

    d3 = ["a", "b"]
    wd3 = WordDistance(d3)
    report(wd3, "a", "b")

    d4 = ["p", "q", "p", "q", "p", "q"]
    wd4 = WordDistance(d4)
    report(wd4, "p", "q")

    d5 = ["m", "z", "z", "z", "n", "m"]
    wd5 = WordDistance(d5)
    report(wd5, "m", "n")
    report(wd5, "z", "n")

    d6 = ["one", "two", "three"]
    wd6 = WordDistance(d6)
    report(wd6, "two", "four")


if __name__ == "__main__":
    main()

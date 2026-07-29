"""LeetCode 243 — Shortest Word Distance (reference oracle).

Same one-pass two-last-seen-indices scan as the Kara version, and the same
`best = n` upper bound so the "word absent" case agrees too.
"""


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


def report(words, word1, word2):
    print(f"{word1} <-> {word2} : {shortest_distance(words, word1, word2)}")


def main():
    d1 = ["practice", "makes", "perfect", "coding", "makes"]
    report(d1, "coding", "practice")
    report(d1, "makes", "coding")

    d2 = ["a", "b", "x", "x", "x", "a", "b"]
    report(d2, "a", "b")
    report(d2, "b", "a")

    d3 = ["a", "b"]
    report(d3, "a", "b")

    d4 = ["p", "q", "p", "q", "p", "q"]
    report(d4, "p", "q")

    d5 = ["m", "z", "z", "z", "n", "m"]
    report(d5, "m", "n")

    d6 = ["one", "two", "three"]
    report(d6, "two", "four")


if __name__ == "__main__":
    main()

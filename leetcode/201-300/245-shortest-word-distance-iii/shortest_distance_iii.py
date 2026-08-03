"""LeetCode 245 - Shortest Word Distance III (reference oracle).

The twist over #243: word1 and word2 may be the SAME word, in which case they
refer to two different occurrences of it.

Unified one-pass: remember the last index that matched EITHER word. A new match
pairs with it whenever the two are genuinely different occurrences of the two
requested words - which, when word1 == word2, is every consecutive pair, and
otherwise only pairs where the words differ.

`best` starts at the list length, the same upper bound #243 and #244 use, so
the "no such pair" case agrees across all three katas.
"""


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


def report(words, word1, word2):
    print(f"{word1} <-> {word2} : {shortest_word_distance(words, word1, word2)}")


def main():
    d1 = ["practice", "makes", "perfect", "coding", "makes"]
    report(d1, "makes", "coding")
    report(d1, "makes", "makes")
    report(d1, "coding", "practice")

    d2 = ["a", "b", "x", "x", "x", "a", "b"]
    report(d2, "a", "b")
    report(d2, "a", "a")
    report(d2, "x", "x")
    report(d2, "b", "b")

    d3 = ["a", "b"]
    report(d3, "a", "b")

    d4 = ["p", "q", "p", "q", "p", "q"]
    report(d4, "p", "q")
    report(d4, "p", "p")

    d5 = ["m", "z", "z", "z", "n", "m"]
    report(d5, "m", "m")
    report(d5, "z", "z")
    report(d5, "m", "n")

    # A word present exactly once has no second occurrence to pair with, so the
    # same-word query falls through to the upper bound.
    d6 = ["one", "two", "three"]
    report(d6, "two", "two")
    report(d6, "two", "four")


if __name__ == "__main__":
    main()

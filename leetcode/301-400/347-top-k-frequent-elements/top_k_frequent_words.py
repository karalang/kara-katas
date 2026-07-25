"""LeetCode 347 — String-keyed sibling (reference oracle).

Same tally / keys-walk / (count desc, word asc) ordering as
top_k_frequent_words.kara.
"""


def top_k_frequent_words(words, k):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    keys = list(counts.keys())
    keys.sort(key=lambda w: (-counts[w], w))
    return keys[:k]


def show(words, k):
    got = top_k_frequent_words(words, k)
    print(f"k={k} -> [{','.join(got)}]")


def main():
    show(["i", "love", "leetcode", "i", "love", "coding"], 2)
    show(["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4)
    show(["pear", "apple", "fig"], 3)
    show(["solo", "solo", "duo"], 5)


if __name__ == "__main__":
    main()

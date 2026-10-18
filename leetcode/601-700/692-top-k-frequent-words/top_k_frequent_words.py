# LeetCode #692: Top K Frequent Words -- count, then sort.
#
# A mirror of top_k_frequent_words.kara (the ★ arm) and its harness.


def top_k_frequent(words, k):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    ranked = sorted(counts.items(), key=lambda e: (-e[1], e[0]))
    return [w for w, _ in ranked[:k]]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(words):
    return "[" + ", ".join('"' + w + '"' for w in words) + "]"


def random_word(longest, alphabet):
    n = 1 + next_random() % longest
    return "".join(chr(97 + next_random() % alphabet) for _ in range(n))


def main():
    global seed
    ex1 = ["i", "love", "leetcode", "i", "love", "coding"]
    print(f"example 1: {show(top_k_frequent(ex1, 2))}")
    ex2 = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
    print(f"example 2: {show(top_k_frequent(ex2, 4))}")
    print(f"one word: {show(top_k_frequent(['kara'], 1))}")
    once = ["ba", "b", "ab", "aa", "a", "abc"]
    print(f"every word once: {show(top_k_frequent(once, 6))}")
    prefixes = ["apple", "app", "ap", "app", "apple", "ap", "a"]
    print(f"equal counts: {show(top_k_frequent(prefixes, 3))}")
    seed = 692
    many = [random_word(3, 3) for _ in range(500)]
    print(f"500 short words, top 10: {show(top_k_frequent(many, 10))}")
    checksum = 0
    letters = 0
    for _ in range(300):
        n = 1 + next_random() % 500
        alphabet = 1 + next_random() % 26
        longest = 1 + next_random() % 10
        words = [random_word(longest, alphabet) for _ in range(n)]
        k = 1 + next_random() % len(set(words))
        for w in top_k_frequent(words, k):
            for b in w.encode():
                checksum = (checksum * 31 + b) % 1000000007
                letters += 1
            checksum = (checksum * 31 + 1) % 1000000007
    print(f"300 random problems: {letters} letters in the answers, checksum {checksum}")


main()

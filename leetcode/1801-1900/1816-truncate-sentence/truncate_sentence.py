# LeetCode #1816: Truncate Sentence -- the ★ arm in Python: the sentence
# split at its spaces, its first k words kept and joined again.


def truncate_sentence(s, k):
    return " ".join(s.split(" ")[:k])


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # LeetCode's three examples
    print(truncate_sentence("Hello how are you Contestant", 4))
    print(truncate_sentence("What is the solution to this problem", 4))
    print(truncate_sentence("chopper is not a tanuki", 5))
    # the edges: one word; every word kept; letters of both cases
    print(f"[{truncate_sentence('a', 1)}] [{truncate_sentence('ab cd', 2)}] [{truncate_sentence('Aa bB Cc', 1)}]")
    # the constraints' most: 500 characters of 250 one-letter words
    longest = " ".join(["x"] * 250)
    print("the most:", len(longest), len(truncate_sentence(longest, 125)), len(truncate_sentence(longest, 250)))
    # 3000 random sentences of 1 to 12 words of 1 to 5 letters
    seed = [1816]
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random(seed) % 12
        words = []
        for _ in range(n):
            m = 1 + next_random(seed) % 5
            word = "".join(chr((65 if next_random(seed) % 2 == 0 else 97) + next_random(seed) % 26) for _ in range(m))
            words.append(word)
        k = 1 + next_random(seed) % n
        cut = truncate_sentence(" ".join(words), k)
        total += len(cut)
        for c in cut:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"3000 random sentences: {total} characters kept, checksum {check}")


main()

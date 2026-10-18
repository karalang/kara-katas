# LeetCode #720: Longest Word in Dictionary -- sorted, one pass.
#
# A mirror of longest_word_in_dictionary.kara (the ★ arm) and its
# harness.


def longest_word(words):
    built = set()
    best = ""
    for word in sorted(words):
        if len(word) == 1 or word[:-1] in built:
            built.add(word)
            if len(word) > len(best):
                best = word
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_word(longest, letters, seed):
    n = 1 + next_random(seed) % longest
    return "".join(chr(97 + next_random(seed) % letters) for _ in range(n))


def grown_words(count, longest, letters, seed):
    words = []
    for _ in range(count):
        if words and next_random(seed) % 3 != 0:
            w = words[next_random(seed) % len(words)]
            if len(w) < 30:
                w += chr(97 + next_random(seed) % letters)
            words.append(w)
        else:
            words.append(random_word(longest, letters, seed))
    return words


def show(words):
    print(f"[{', '.join(words)}] -> \"{longest_word(words)}\"")


def main():
    show(["w", "wo", "wor", "worl", "world"])
    show(["a", "banana", "app", "appl", "ap", "apply", "apple"])
    show(["a"])
    show(["abc"])
    show(["ab", "abc"])
    show(["z", "y", "x"])
    show(["b", "ba", "a"])
    show(["a", "ac", "ab", "abd", "acd"])
    show(["a", "ab", "abc", "b", "bc", "bcd", "bcde"])
    show(["m", "mo", "mon", "moon", "mood", "moo"])
    chain = []
    a = b = ""
    for i in range(30):
        a += "q"
        b += "b"
        chain.append(a)
        if i != 28:
            chain.append(b)
    print(f"two 30-letter chains, one broken -> {longest_word(chain)}")
    seed = [720]
    grown = grown_words(1000, 3, 3, seed)
    print(f"1000 grown words from 3 letters -> {longest_word(grown)}")
    grown26 = grown_words(1000, 4, 26, seed)
    print(f"1000 grown words from 26 letters -> {longest_word(grown26)}")
    fresh = [random_word(30, 26, seed) for _ in range(1000)]
    print(f"1000 random words of up to 30 letters -> \"{longest_word(fresh)}\"")
    total = 0
    for _ in range(300):
        count = 1 + next_random(seed) % 40
        letters = 1 + next_random(seed) % 4
        words = grown_words(count, 3, letters, seed)
        answer = longest_word(words)
        total = (total * 131 + len(answer)) % 1000000007
        for c in answer:
            total = (total * 31 + ord(c)) % 1000000007
    print(f"300 random dictionaries: checksum {total}")


main()

# LeetCode #2063: Vowels of All Substrings -- Python mirror of the ★ arm
# (vowels.kara): each vowel at place `i` of `n` letters is in `(i + 1) *
# (n - i)` substrings, and the answer is their sum.


def count_vowels(word):
    n = len(word)
    total = 0
    for i, c in enumerate(word):
        if c in "aeiou":
            total += (i + 1) * (n - i)
    return total


seed = 2063


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` letters, each a vowel with chance `p` in 100, else one of `bcdxyz`
def word_of(n, p):
    out = []
    for _ in range(n):
        if next_random() % 100 < p:
            out.append("aeiou"[next_random() % 5])
        else:
            out.append("bcdxyz"[next_random() % 6])
    return "".join(out)


def main():
    examples = ["aba", "abc", "ltcd", "a", "b", "aeiou", "zzzzz", "noosabasboosa"]
    for w in examples:
        print(f"{w} -> {count_vowels(w)}")
    # 500 words of 1 to 300 letters, vowels with chance 0 to 100 in 100
    check = 0
    for _ in range(500):
        n = next_random() % 300 + 1
        p = next_random() % 101
        check = (check * 31 + count_vowels(word_of(n, p))) % 1000000007
    print(f"500 words: checksum {check}")
    # the largest the constraints allow: 100000 letters, all vowels, then
    # vowels with chance 40 in 100
    print(f"100000 vowels -> {count_vowels(word_of(100000, 100))}")
    print(f"100000 letters -> {count_vowels(word_of(100000, 40))}")


main()

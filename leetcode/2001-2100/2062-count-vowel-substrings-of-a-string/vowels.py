# LeetCode #2062: Count Vowel Substrings of a String -- Python mirror of
# the ★ arm (vowels.kara): every start, extended while the letters are
# vowels, the vowels met kept in a set, each end counted once all five
# are in it.


def count_vowel_substrings(word):
    count = 0
    for i in range(len(word)):
        met = set()
        for j in range(i, len(word)):
            if word[j] not in "aeiou":
                break
            met.add(word[j])
            if len(met) == 5:
                count += 1
    return count


seed = 2062


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# `n` letters, each a vowel with chance `p` in 100, else one of `xyz`
def word_of(n, p):
    out = []
    for _ in range(n):
        if next_random() % 100 < p:
            out.append("aeiou"[next_random() % 5])
        else:
            out.append("xyz"[next_random() % 3])
    return "".join(out)


def main():
    examples = ["aeiouu", "unicornarihan", "cuaieuouac", "bbaeixoubb", "a", "aeiou",
                "uoiea", "aaeeiioouu", "xaeioux", "aeioaeiouaeiou"]
    for w in examples:
        print(f"{w} -> {count_vowel_substrings(w)}")
    # 500 words of 1 to 100 letters, vowels with chance 50 to 100 in 100
    total = 0
    check = 0
    for _ in range(500):
        n = next_random() % 100 + 1
        p = next_random() % 51 + 50
        a = count_vowel_substrings(word_of(n, p))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"500 words: sum {total}, checksum {check}")
    # a word of 100 vowels, then `aeiou` twenty times
    print(f"100 vowels -> {count_vowel_substrings(word_of(100, 100))}")
    print(f"aeiou x 20 -> {count_vowel_substrings('aeiou' * 20)}")


main()

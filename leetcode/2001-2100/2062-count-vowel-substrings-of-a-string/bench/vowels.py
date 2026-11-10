# LeetCode #2062: Count Vowel Substrings of a String -- Python mirror of
# the ★ arm's benchmark (vowels.kara): 20000 words of 100 letters, each a
# vowel with chance 90 in 100, else one of `xyz`.


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


def word_of(n, p):
    out = []
    for _ in range(n):
        if next_random() % 100 < p:
            out.append("aeiou"[next_random() % 5])
        else:
            out.append("xyz"[next_random() % 3])
    return "".join(out)


def main():
    total = 0
    check = 0
    for _ in range(20000):
        a = count_vowel_substrings(word_of(100, 90))
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"20000 words: sum {total}, checksum {check}")


main()

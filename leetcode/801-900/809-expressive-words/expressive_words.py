# LeetCode 809 -- Expressive Words: mirrors the harness of
# expressive_words.kara with the ★ arm's two pointers over the groups.
seed = 809


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def stretchy(s, word):
    i = j = 0
    while i < len(s) and j < len(word):
        c = s[i]
        if word[j] != c:
            return False
        from_i = i
        while i < len(s) and s[i] == c:
            i += 1
        from_j = j
        while j < len(word) and word[j] == c:
            j += 1
        in_s = i - from_i
        in_word = j - from_j
        if in_s < in_word or (in_s > in_word and in_s < 3):
            return False
    return i == len(s) and j == len(word)


def expressive_words(s, words):
    return sum(1 for w in words if stretchy(s, w))


def show(s, words):
    print(f"s = \"{s}\", words = [{', '.join(words)}] -> {expressive_words(s, words)}")


def random_groups(groups, letters, longest):
    out = []
    last = 26
    for _ in range(groups):
        c = next_random() % letters
        if c == last:
            c = (c + 1) % letters
        last = c
        out.append((chr(97 + c), 1 + next_random() % longest))
    return out


def spell(groups):
    return "".join(c * n for c, n in groups)


def main():
    show("heeellooo", ["hello", "hi", "helo"])
    show("zzzzzyyyyy", ["zzyy", "zy", "zyy"])
    show("dddiiiinnssssssoooo", ["dinnssoo", "ddinso", "ddiinnso", "ddiinnssoo", "ddiinso", "dinsoo", "ddiinsso", "dinssoo", "dinso"])
    show("abcd", ["abc", "abcd", "abcde", "abdc"])
    show("aaa", ["a", "aa", "aaa", "aaaa", "b"])
    show("aa", ["a", "aa", "aaa"])
    show("a", ["a", "b", "aa"])
    big = [(chr(97 + g % 2 * 3 + g % 3), 5) for g in range(20)]
    s = spell(big)
    words = [spell([(big[g][0], 1 + (i + 3 * g) % 6) for g in range(20)]) for i in range(100)]
    print(f"100 letters, 100 words -> {expressive_words(s, words)}")
    total = 0
    check = 0
    for r in range(300):
        groups = random_groups(1 + next_random() % 6, 3, 5)
        s = spell(groups)
        words = []
        for _ in range(8):
            if next_random() % 4 == 0:
                words.append(spell(random_groups(1 + next_random() % 6, 3, 3)))
            else:
                words.append(spell([(c, 1 + next_random() % 4) for c, _ in groups]))
        n = expressive_words(s, words)
        total += n
        check = (check * 131 + n + r) % 1000000007
    print(f"300 random rounds of 8 words: {total} stretchy, checksum {check}")


main()

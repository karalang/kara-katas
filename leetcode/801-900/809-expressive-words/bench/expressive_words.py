# LeetCode 809 -- Expressive Words: the bench, with the ★ arm's two
# pointers over the groups.
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
    count = 0
    for w in words:
        if stretchy(s, w):
            count += 1
    return count


def spell(groups):
    return "".join(c * n for c, n in groups)


def main():
    texts = []
    lists = []
    for _ in range(64):
        groups = []
        last = 26
        for _ in range(25):
            c = next_random() % 5
            if c == last:
                c = (c + 1) % 5
            last = c
            groups.append((chr(97 + c), 1 + next_random() % 4))
        words = []
        for _ in range(100):
            if next_random() % 4 == 0:
                n = 1 + next_random() % 100
                words.append("".join(chr(97 + next_random() % 5) for _ in range(n)))
            else:
                shrunk = [(c, 1 + next_random() % n if n >= 3 else n) for c, n in groups]
                if next_random() % 3 == 0:
                    g = next_random() % 25
                    shrunk[g] = (shrunk[g][0], groups[g][1] + 1)
                words.append(spell(shrunk))
        texts.append(spell(groups))
        lists.append(words)
    rounds = 200000
    total = 0
    check = 0
    for r in range(rounds):
        n = expressive_words(texts[r % 64], lists[r % 64])
        total += n
        check = (check * 131 + n + r) % 1000000007
    print(f"{rounds} rounds of 100 words: {total} stretchy, checksum {check}")


main()

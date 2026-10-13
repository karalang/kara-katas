# LeetCode #527: Word Abbreviation -- Python mirror of the ★ arm (grow
# clashing prefixes); see words_abbreviation.kara. Same algorithm, same
# harness, same output.


def abbreviate(word, k):
    n = len(word)
    if k >= n - 2:
        return word
    return f"{word[:k]}{n - 1 - k}{word[n - 1]}"


def words_abbreviation(words):
    n = len(words)
    prefix = [1] * n
    abbr = [abbreviate(w, 1) for w in words]
    for i in range(n):
        while True:
            clash = [j for j in range(i + 1, n) if abbr[j] == abbr[i]]
            if not clash:
                break
            clash.append(i)
            for j in clash:
                prefix[j] += 1
                abbr[j] = abbreviate(words[j], prefix[j])
    return abbr


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def random_words(count, shortest, longest, letters):
    seen = set()
    words = []
    for _ in range(count * 4):
        if len(words) == count:
            break
        word = random_word(shortest + next_random() % (longest - shortest + 1), letters)
        if word not in seen:
            seen.add(word)
            words.append(word)
    return words


def fmt(words):
    return "[" + ", ".join(words) + "]"


def show(words):
    print(f"{fmt(words)}: {fmt(words_abbreviation(words))}")


def main():
    global seed
    show(["like", "god", "internal", "me", "internet", "interval", "intension", "face", "intrusion"])
    show(["aa", "aaa"])
    show(["abcdef", "abndef"])
    show(["abcdefghijklm", "abcdefghijxlm", "axcdefghijklm"])
    show(["wxyz", "wyyz", "wzyz"])
    seed = 527
    kept = 0
    letters_out = 0
    checksum = 0
    for _ in range(500):
        count = 2 + next_random() % 39
        letters = 1 + next_random() % 3
        words = random_words(count, 2, 12, letters)
        abbr = words_abbreviation(words)
        for i in range(len(abbr)):
            if abbr[i] == words[i]:
                kept += 1
            letters_out += len(abbr[i])
            for b in abbr[i].encode():
                checksum = (checksum * 31 + b) % 1000000007
    print(f"500 random lists: {kept} words kept whole, {letters_out} letters, checksum {checksum}")
    words = random_words(400, 40, 60, 2)
    abbr = words_abbreviation(words)
    longest = max(len(a) for a in abbr)
    total = sum(len(a) for a in abbr)
    print(f"{len(words)} words of 40 to 60 letters: {total} letters, longest {longest}, first {abbr[0]}")


main()

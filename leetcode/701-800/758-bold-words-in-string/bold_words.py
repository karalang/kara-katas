# LeetCode 758 — Bold Words in String: Python mirror of the ★ arm and its
# harness (same marking by repeated find, same output).


def bold_words(words, s):
    n = len(s)
    bold = [False] * n
    for word in words:
        start = 0
        while start < n:
            at = s.find(word, start)
            if at < 0:
                break
            for i in range(at, at + len(word)):
                bold[i] = True
            start = at + 1
    out = []
    for i in range(n):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")
        out.append(s[i])
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")
    return "".join(out)


seed = 758


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def show(words, s):
    print(f"[{', '.join(words)}] {s} -> {bold_words(words, s)}")


def main():
    show(["ab", "bc"], "aabcd")
    show(["ab", "cb"], "aabcd")
    show([], "abc")
    show(["abc"], "abc")
    show(["ab", "cd"], "abcd")
    show(["aa"], "aaa")
    show(["zz"], "abc")
    show(["b"], "abcba")
    show(["abcdefghij"], "abc")
    show(["e", "cde", "bcdef"], "abcdefg")
    tags = 0
    marks = 0
    check = 0
    for _ in range(300):
        letters = 2 + next_random() % 5
        length = 1 + next_random() % 500
        s = random_text(length, letters)
        count = next_random() % 51
        longest = 1 + next_random() % 10
        words = []
        for _ in range(count):
            size = 1 + next_random() % longest
            words.append(random_text(size, letters + 1))
        answer = bold_words(words, s)
        tags += (len(answer) - len(s)) // 7
        for c in answer:
            check = (check * 31 + ord(c)) % 1000000007
        marks += len(answer) - len(s)
    print(f"300 random strings: {tags} bold runs, {marks} tag characters, checksum {check}")


main()

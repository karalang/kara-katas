# LeetCode 758 — Bold Words in String: benchmark, the ★ arm.


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


def main():
    rounds = 20000
    total = 0
    check = 0
    for _ in range(rounds):
        s = random_text(500, 4)
        words = []
        for _ in range(50):
            size = 1 + next_random() % 10
            words.append(random_text(size, 5))
        answer = bold_words(words, s)
        total += len(answer)
        for c in answer.encode():
            check = (check * 31 + c) % 1000000007
    print(f"{rounds} strings of 500 letters: {total} characters out, checksum {check}")


main()

# Benchmark mirror for #616: the same workload and algorithm as
# add_bold_tag.kara (mark, then write).


def add_bold_tag(s, words):
    n = len(s)
    bold = [False] * n
    for i in range(n):
        for word in words:
            if s.startswith(word, i):
                for k in range(i, i + len(word)):
                    bold[k] = True
    out = []
    for i in range(n):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")
        out.append(s[i])
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")
    return "".join(out)


seed = 616


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(size):
    return "".join(chr(97 + step() % 4) for _ in range(size))


def main():
    cases = 20
    rounds = 1000
    texts = []
    lists = []
    for _ in range(cases):
        s = random_text(1000)
        words = []
        while len(words) < 100:
            length = 5 + step() % 10
            if len(words) % 2 == 0:
                at = step() % (1000 - length)
                w = s[at:at + length]
            else:
                w = random_text(length)
            if w not in words:
                words.append(w)
        texts.append(s)
        lists.append(words)
    total = 0
    checksum = 0
    for r in range(rounds):
        c = (r * 7) % cases
        out = add_bold_tag(texts[c], lists[c])
        total += len(out)
        for ch in out:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{cases} cases, {rounds} rounds: {total} characters, checksum {checksum}")


main()

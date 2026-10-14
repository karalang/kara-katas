# LeetCode #616: Add Bold Tag in String -- Python mirror of the ★ arm
# (mark, then write); see add_bold_tag.kara.


def add_bold_tag(s, words):
    n = len(s)
    bold = [False] * n
    for i in range(n):
        for word in words:
            if s[i:n].startswith(word):
                for k in range(i, i + len(word)):
                    bold[k] = True
    out = []
    for i in range(n):
        if bold[i] and (i == 0 or not bold[i - 1]):
            out.append("<b>")
        out.append(s[i:i + 1])
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            out.append("</b>")
    return "".join(out)


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(s, words):
    print(f"{s} [{', '.join(words)}] -> {add_bold_tag(s, words)}")


def random_text(size, kinds, seed):
    return "".join(chr(97 + step(seed) % kinds) for _ in range(size))


def runs(out):
    return sum(1 for i in range(len(out)) if out[i:].startswith("<b>"))


def main():
    show("abcxyz123", ["abc", "123"])
    show("aaabbb", ["aa", "b"])
    show("abc", [])
    show("ab", ["abc"])
    show("abcd", ["ab", "cd"])
    show("aaaa", ["aaa"])
    show("xyz", ["xyz"])
    show("abcabc", ["cab", "zz"])
    show("abcdef", ["bcde", "cd"])
    show("a", ["a"])
    show("a1b2c3", ["1", "3", "b2"])
    seed = [616]
    total = tags = checksum = 0
    for _ in range(300):
        kinds = 2 + step(seed) % 3
        size = 1 + step(seed) % 30
        s = random_text(size, kinds, seed)
        words = []
        for _ in range(step(seed) % 6):
            length = 1 + step(seed) % 4
            w = random_text(length, kinds, seed)
            if w not in words:
                words.append(w)
        out = add_bold_tag(s, words)
        total += len(out)
        tags += runs(out)
        for c in out:
            checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"300 random strings: {total} characters, {tags} bold runs, checksum {checksum}")
    big = random_text(1000, 4, seed)
    words = []
    while len(words) < 100:
        length = 5 + step(seed) % 10
        if step(seed) % 2 == 0:
            at = step(seed) % (1000 - length)
            w = big[at:at + length]
        else:
            w = random_text(length, 4, seed)
        if w not in words:
            words.append(w)
    out = add_bold_tag(big, words)
    h = 0
    for c in out:
        h = (h * 31 + ord(c)) % 1000000007
    print(f"1000 characters, 100 words: {len(out)} characters, {runs(out)} bold runs, checksum {h}")


main()

# LeetCode #2788: Split Strings by Separator -- the ★ arm in Python
# (split.kara): each word split at the separator, the empty pieces
# dropped.


def split_words_by_separator(words, separator):
    return [piece for w in words for piece in w.split(separator) if piece]


seed = 2788


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(letters[next_random() % len(letters)] for _ in range(n))


def fold(pieces, check):
    for p in pieces:
        for b in p.encode():
            check = (check * 31 + b) % 1000000007
        check = (check * 31 + 1) % 1000000007
    return check


def show(pieces):
    return "[" + ", ".join(pieces) + "]"


def main():
    print(show(split_words_by_separator(["one.two.three", "four.five", "six"], ".")))
    print(show(split_words_by_separator(["$easy$", "$problem$"], "$")))
    print(show(split_words_by_separator(["|||"], "|")))
    print(show(split_words_by_separator(["a#b", "#c#", "d##e", "f"], "#")))
    long = ["a@" * 10 for _ in range(100)]
    print(len(split_words_by_separator(long, "@")))
    pieces = 0
    check = 0
    for _ in range(3000):
        count = next_random() % 5 + 1
        words = []
        for _ in range(count):
            n = next_random() % 8 + 1
            words.append(random_text(n, "ab.|"))
        separator = "." if next_random() % 2 == 0 else "|"
        got = split_words_by_separator(words, separator)
        pieces += len(got)
        check = fold(got, check)
    print(f"3000 small cases: {pieces} pieces, checksum {check}")


main()

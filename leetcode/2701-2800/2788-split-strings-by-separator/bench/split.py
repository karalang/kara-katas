# LeetCode #2788: Split Strings by Separator -- the bench in Python: the ★
# arm over 20000 lists of 100 words of 20 characters from a, b, c and the
# six separators, each split by one of them, all drawn first, then each
# answered 10 times.


def split_words_by_separator(words, separator):
    return [piece for w in words for piece in w.split(separator) if piece]


seed = 2788


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 20000
    rounds = 10
    letters = "abc.,|$#@"
    separators = ".,|$#@"
    cases = []
    for _ in range(count):
        words = ["".join(letters[next_random() % 9] for _ in range(20)) for _ in range(100)]
        cases.append((words, separators[next_random() % 6]))
    pieces = 0
    check = 0
    for r in range(rounds):
        for words, separator in cases:
            got = split_words_by_separator(words, separator)
            pieces += len(got)
            for p in got:
                check = (check * 31 + len(p) + r) % 1000000007
    print(f"{count} lists of 100 words, {rounds} rounds: {pieces} pieces, checksum {check}")


main()

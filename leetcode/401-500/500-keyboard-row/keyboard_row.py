# LeetCode #500: Keyboard Row -- a row number for every letter.
# Mirrors keyboard_row.kara (the ★ arm); output is byte-identical.


def find_words(words):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    row_of = [0] * 26
    for r in range(3):
        for ch in rows[r]:
            row_of[ord(ch) - ord("a")] = r
    out = []
    for word in words:
        first = -1
        one_row = True
        for ch in word.lower():
            r = row_of[ord(ch) - ord("a")]
            if first < 0:
                first = r
            elif r != first:
                one_row = False
                break
        if one_row:
            out.append(word)
    return out


def fmt(v):
    return "[" + ", ".join(v) + "]"


def show(name, words):
    print(f"{name}: {fmt(words)} -> {fmt(find_words(words))}")


seed = 500


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", ["Hello", "Alaska", "Dad", "Peace"])
    show("example 2", ["omk"])
    show("example 3", ["adsdf", "sfd"])
    show("one letter each", ["a", "Q", "z", "M"])
    show("whole rows", ["QWERTYUIOP", "asdfghjkl", "ZxCvBnM", "qaz"])
    show("mixed case", ["TyPeWrItEr", "Typewriters", "FLASK", "flasks"])
    show("keyboard row", ["abc", "Keyboard", "Row"])
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "abcdefghijklmnopqrstuvwxyz"]
    count = 300
    kept = 0
    letters = 0
    checksum = 0
    for _ in range(count):
        size = 1 + next_random() % 20
        words = []
        for _ in range(size):
            pool = 3 if next_random() % 3 == 0 else next_random() % 3
            chars = list(rows[pool])
            length = 1 + next_random() % 12
            word = ""
            for _ in range(length):
                ch = chars[next_random() % len(chars)]
                if next_random() % 4 == 0:
                    word += ch.upper()
                else:
                    word += ch
            words.append(word)
        for word in find_words(words):
            kept += 1
            letters += len(word)
            for ch in word:
                checksum = (checksum * 31 + ord(ch)) % 1000000007
    print(f"{count} random lists: {kept} words kept, {letters} letters, checksum {checksum}")


main()

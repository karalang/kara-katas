# LeetCode 819 — Most Common Word, by a map of counts.
#
# Mirrors most_common_word.kara: lower every letter and turn everything
# else into a space, count each word that is not banned, and return the
# word counted most, the first alphabetically of two counted as often.


def most_common_word(paragraph, banned):
    cleaned = "".join(c.lower() if c.isascii() and c.isalpha() else " " for c in paragraph)
    ruled_out = set(banned)
    counts = {}
    for word in cleaned.split():
        if word not in ruled_out:
            counts[word] = counts.get(word, 0) + 1
    best, most = "", 0
    for word, n in counts.items():
        if n > most or (n == most and word < best):
            best, most = word, n
    return best


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(paragraph, banned):
    answer = most_common_word(paragraph, banned)
    print(f"{paragraph} / [{', '.join(banned)}] -> {answer}")


def main():
    show("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"])
    show("a.", [])
    show("a, a, a, a, b,b,b,c, c", ["a"])
    show("Bob. hIt, baLl", ["bob", "hit"])
    show("abc abc? abcd the jeff!", ["abc", "abcd", "jeff"])
    show("tie Tie apple APPLE zebra", [])
    show("j. t? s' J!", ["s", "t"])
    vocabulary = ["the", "car", "bob", "ball", "hit", "far", "a", "it", "was", "fly", "sun", "moon"]
    marks = [" ", " ", " ", ", ", ". ", "! ", "? ", "; ", "' ", ","]
    rng = Random(819)
    big = ""
    while len(big) < 990:
        word = vocabulary[rng.next() % 12]
        if rng.next() % 3 == 0:
            word = word.upper()
        big += word
        big += marks[rng.next() % 10]
    many = [f"w{k}" for k in range(100)] + ["the"]
    print(f"{len(big)} characters, {len(many)} banned -> {most_common_word(big, many)}")
    total = 0
    check = 0
    for _ in range(300):
        paragraph = ""
        count = 1 + rng.next() % 20
        for _ in range(count):
            word = vocabulary[rng.next() % 6]
            if rng.next() % 4 == 0:
                word = word.upper()
            paragraph += word
            paragraph += marks[rng.next() % 10]
        paragraph += "far"
        banned = [vocabulary[k] for k in range(5) if rng.next() % 4 == 0]
        answer = most_common_word(paragraph, banned)
        total += len(answer)
        for b in answer.encode():
            check = (check * 131 + b) % 1000000007
    print(f"300 random paragraphs: total {total}, checksum {check}")


main()

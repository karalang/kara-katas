# Benchmark for #425: mirror of word_squares.kara (a map of prefixes).
import sys

sys.setrecursionlimit(10000)


def word_squares(words):
    length = len(words[0])
    by_prefix = {}
    for i, word in enumerate(words):
        for k in range(length):
            by_prefix.setdefault(word[:k], []).append(i)
    found = []
    rows = []

    def extend():
        r = len(rows)
        if r == length:
            found.append(list(rows))
            return
        prefix = "".join(row[r] for row in rows)
        for i in by_prefix.get(prefix, ()):
            rows.append(words[i])
            extend()
            rows.pop()

    extend()
    return found


seed = 425


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    return "".join(chr(97 + step() % 16) for _ in range(4))


rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 20
n = 1000
seen = set()
words = []
while len(words) < n:
    word = random_word()
    if word not in seen:
        seen.add(word)
        words.append(word)
total = 0
checksum = 0
for r in range(rounds):
    word = random_word()
    while word in seen:
        word = random_word()
    at = r * 389 % n
    seen.discard(words[at])
    seen.add(word)
    words[at] = word
    squares = word_squares(words)
    total += len(squares)
    for square in squares:
        checksum = (checksum * 31 + ord(square[0][0]) + ord(square[3][3])) % 1000000007
print(f"{rounds} rounds on {n} words: {total} squares, checksum {checksum}")

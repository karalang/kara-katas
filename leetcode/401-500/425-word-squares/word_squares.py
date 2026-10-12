# LeetCode #425: Word Squares -- mirror of word_squares.kara (a map of
# prefixes).


def word_squares(words):
    length = len(words[0])
    by_prefix = {}
    for i, word in enumerate(words):
        for k in range(length + 1):
            by_prefix.setdefault(word[:k], []).append(i)
    found = []
    rows = []

    def extend():
        r = len(rows)
        if r == length:
            found.append(list(rows))
            return
        prefix = "".join(row[r] for row in rows)
        for i in by_prefix.get(prefix, []):
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


def lines(squares):
    return sorted("/".join(square) for square in squares)


def show(text):
    found = lines(word_squares(text.split()))
    print(f'"{text}": {len(found)} [{", ".join(found)}]')


show("area lead wall lady ball")
show("abat baba atan atal")
show("a")
show("ab")
show("ab ba")
show("aa")
show("abc bde cef")
show("abc bca cab")
show("xy yz")
show("ab bc cd")
total = 0
checksum = 0
for _ in range(300):
    length = 2 + step() % 3
    wanted = 3 + step() % 28
    seen = set()
    words = []
    tries = 0
    while len(words) < wanted and tries < 200:
        tries += 1
        word = "".join(chr(97 + step() % 3) for _ in range(length))
        if word not in seen:
            seen.add(word)
            words.append(word)
    found = lines(word_squares(words))
    total += len(found)
    for line in found:
        for ch in line:
            checksum = (checksum * 31 + ord(ch)) % 1000000007
print(f"300 random lists: {total} squares, checksum {checksum}")

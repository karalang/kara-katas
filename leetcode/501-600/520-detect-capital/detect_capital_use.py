# LeetCode #520: Detect Capital -- mirror of the ★ arm (count the
# capitals); see detect_capital_use.kara.


def detect_capital_use(word):
    capitals = sum(1 for c in word if c.isupper())
    return capitals == 0 or capitals == len(word) or (capitals == 1 and word[0].isupper())


seed = 520


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# A random word of 1 to 100 letters: all capitals, all lower case, a
# capital then lower case, any mix, or one of the first three with one
# letter's case turned.
def random_word():
    n = 1 + next_random() % 100
    kind = next_random() % 5
    shape = next_random() % 3 if kind == 4 else kind
    letters = []
    for i in range(n):
        c = chr(97 + next_random() % 26)
        if shape == 0:
            capital = True
        elif shape == 1:
            capital = False
        elif shape == 2:
            capital = i == 0
        else:
            capital = next_random() % 2 == 0
        letters.append(c.upper() if capital else c)
    if kind == 4:
        at = next_random() % n
        letters[at] = letters[at].lower() if letters[at].isupper() else letters[at].upper()
    return "".join(letters)


def main():
    words = ["USA", "FlaG", "leetcode", "Google", "g", "G", "gG", "Gg", "GG", "gg", "GGg", "ggG", "mL", "aBC", "ABc", "AbC"]
    for w in words:
        print(f"{w}: {'true' if detect_capital_use(w) else 'false'}")
    right = 0
    checksum = 0
    for i in range(3000):
        word = random_word()
        if detect_capital_use(word):
            right += 1
            checksum = (checksum * 31 + (i + 1) * len(word)) % 1000000007
    print(f"3000 random words: {right} use capitals right, checksum {checksum}")


main()

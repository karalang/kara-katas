# LeetCode #1662 bench: the ★ arm, two cursors, one in each array.
#
# 20 pairs of word arrays spelling texts of 10^6 letters, cut into words
# of about 8 letters, are built first; half spell the same text and half
# differ in the last letter. Then each pair is checked 20 times.


def array_strings_are_equal(word1, word2):
    w1 = i1 = 0
    w2 = i2 = 0
    while w1 < len(word1) and w2 < len(word2):
        a = word1[w1]
        b = word2[w2]
        if a[i1] != b[i2]:
            return False
        i1 += 1
        i2 += 1
        if i1 == len(a):
            w1 += 1
            i1 = 0
        if i2 == len(b):
            w2 += 1
            i2 = 0
    return w1 == len(word1) and w2 == len(word2)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n):
    return bytearray(ord("a") + next_random() % 2 for _ in range(n))


def cut(text):
    words = []
    start = 0
    for i in range(1, len(text)):
        if next_random() % 8 == 0:
            words.append(text[start:i].decode())
            start = i
    words.append(text[start:].decode())
    return words


def main():
    global seed
    pairs = 20
    letters = 1000000
    rounds = 20
    seed = 1662
    cases = []
    for k in range(pairs):
        text = random_text(letters)
        other = bytearray(text)
        if k % 2 == 1:
            other[letters - 1] = ord("b") if other[letters - 1] == ord("a") else ord("a")
        cases.append((cut(text), cut(other)))
    equal = 0
    check = 0
    for r in range(rounds):
        for word1, word2 in cases:
            answer = array_strings_are_equal(word1, word2)
            if answer:
                equal += 1
            check = (check * 31 + (2 if answer else 1) + len(word1) + len(word2) + r) % 1000000007
    print(f"{pairs} pairs of {letters} letters, {rounds} rounds: {equal} equal, checksum {check}")


main()

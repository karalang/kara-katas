# LeetCode 748 — Shortest Completing Word, bench: the ★ arm (letter
# counts) on a list of 1000 words that keeps changing, against a new
# plate each round. Mirrors shortest_completing_word.kara.


def shortest_completing_word(license_plate, words):
    need = [0] * 26
    for c in license_plate:
        if 'a' <= c <= 'z':
            need[ord(c) - 97] += 1
        elif 'A' <= c <= 'Z':
            need[ord(c) - 65] += 1
    best = -1
    for i, w in enumerate(words):
        if best != -1 and len(w) >= len(words[best]):
            continue
        have = [0] * 26
        for c in w:
            have[ord(c) - 97] += 1
        if all(have[c] >= need[c] for c in range(26)):
            best = i
    return words[best]


seed = 748


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word():
    n = 1 + next_random() % 15
    return ''.join(chr(97 + next_random() % 6) for _ in range(n))


def random_plate():
    n = 1 + next_random() % 7
    s = []
    for _ in range(n):
        kind = next_random() % 6
        if kind < 2:
            code = 97 + next_random() % 6
        elif kind < 4:
            code = 65 + next_random() % 6
        elif kind == 4:
            code = 48 + next_random() % 10
        else:
            code = 32
        s.append(chr(code))
    return ''.join(s)


def main():
    rounds = 100000
    n = 1000
    words = [random_word() for _ in range(n)]
    letters = 0
    check = 0
    for _ in range(rounds):
        for _ in range(5):
            i = next_random() % (n - 1)
            words[i] = random_word()
        plate = random_plate()
        last = ''.join(c.lower() for c in plate if c.isascii() and c.isalpha())
        if not last:
            last = 'a'
        words[n - 1] = last
        got = shortest_completing_word(plate, words)
        letters += len(got)
        for c in got:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"{rounds} plates against 1000 words: answers {letters} letters long in all, checksum {check}")


main()

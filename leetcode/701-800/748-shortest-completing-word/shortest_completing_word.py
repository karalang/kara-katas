# LeetCode 748 — Shortest Completing Word, letter counts.
# Mirror of shortest_completing_word.kara (the ★ arm); same output, byte for byte.


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


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(plate, text):
    print(f"\"{plate}\", [{text}] -> {shortest_completing_word(plate, text.split(' '))}")


def random_word(rng, longest, letters):
    n = 1 + rng.next() % longest
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def random_plate(rng, letters):
    s = []
    n = 1 + rng.next() % 7
    for _ in range(n):
        kind = rng.next() % 6
        if kind < 2:
            code = 97 + rng.next() % letters
        elif kind < 4:
            code = 65 + rng.next() % letters
        elif kind == 4:
            code = 48 + rng.next() % 10
        else:
            code = 32
        s.append(chr(code))
    return "".join(s)


def plate_word(plate):
    s = "".join(c for c in plate.lower() if 'a' <= c <= 'z')
    return s if s else "a"


def checksum(check, word):
    for c in word:
        check = (check * 31 + ord(c)) % 1000000007
    return check


def main():
    show("1s3 PSt", "step steps stripe stepple")
    show("1s3 456", "looks pest stew show")
    show("Ah71752", "suggest letter of husband easy education drug prevent writer old")
    show("OgEu755", "enough these play wide wonder box arrive money tax thus")
    show("iMSlpe4", "claim consumer student camera public never wonder simple thought use")
    show("aB", "abc ab ba")
    show("123 456", "pear go me")
    show("AAa", "aa banana aaa")

    rng = Rng(748)
    lengths = 0
    check = 0
    for _ in range(30):
        words = [random_word(rng, 15, 6) for _ in range(999)]
        plate = random_plate(rng, 3)
        words.append(plate_word(plate))
        got = shortest_completing_word(plate, words)
        lengths += len(got)
        check = checksum(check, got)
    print(f"30 lists of 1000 words: answers {lengths} letters long in all, checksum {check}")

    total = 0
    check = 0
    for _ in range(300):
        n = 1 + rng.next() % 8
        words = [random_word(rng, 5, 3) for _ in range(n)]
        plate = random_plate(rng, 3)
        words.append(plate_word(plate))
        got = shortest_completing_word(plate, words)
        total += len(got)
        check = checksum(check, got)
    print(f"300 random lists: answers {total} letters long in all, checksum {check}")


main()

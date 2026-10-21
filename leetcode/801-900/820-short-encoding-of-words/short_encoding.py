# LeetCode 820 — Short Encoding of Words, by a set of the words.
#
# Mirrors short_encoding.kara: put every word in a set, take
# out every proper suffix of every word, and the words left each cost
# their length and a '#'.


def minimum_length_encoding(words):
    kept = set(words)
    for word in words:
        for k in range(1, len(word)):
            kept.discard(word[k:])
    return sum(len(word) + 1 for word in kept)


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_word(rng, letters, longest):
    length = 1 + rng.next() % longest
    return "".join(chr(ord("a") + rng.next() % letters) for _ in range(length))


def show(words):
    print(f"[{', '.join(words)}] -> {minimum_length_encoding(words)}")


def main():
    show(["time", "me", "bell"])
    show(["t"])
    show(["me", "me"])
    show(["time", "time", "me", "ime"])
    show(["a", "b", "c"])
    show(["abc", "bc", "c", "xbc"])
    show(["me", "time", "emit"])
    show(["ab", "ba", "aba", "bab"])
    rng = Random(820)
    few = [random_word(rng, 3, 7) for _ in range(2000)]
    many = [random_word(rng, 26, 7) for _ in range(2000)]
    print(f"2000 words of 3 letters -> {minimum_length_encoding(few)}")
    print(f"2000 words of 26 letters -> {minimum_length_encoding(many)}")
    total = 0
    check = 0
    for _ in range(300):
        count = 1 + rng.next() % 20
        words = [random_word(rng, 2, 5) for _ in range(count)]
        answer = minimum_length_encoding(words)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random lists: total {total}, checksum {check}")


main()

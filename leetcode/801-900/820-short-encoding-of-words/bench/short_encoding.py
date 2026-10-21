# Benchmark for #820: Short Encoding of Words -- the ★ arm (a set of the words).
#
# Mirrors short_encoding.kara: put every word in a set, take out every
# proper suffix of every word, and the words left each cost their length
# and a '#'.


def minimum_length_encoding(words):
    kept = set(words)
    for word in words:
        for k in range(1, len(word)):
            kept.discard(word[k:])
    total = 0
    for word in kept:
        total += len(word) + 1
    return total


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_word(rng, letters, longest):
    length = 1 + rng.next() % longest
    return "".join(chr(ord("a") + rng.next() % letters) for _ in range(length))


def main():
    count = 64
    rounds = 12000
    rng = Random(820)
    lists = [[random_word(rng, 5, 7) for _ in range(2000)] for _ in range(count)]
    total = 0
    checksum = 0
    for r in range(rounds):
        answer = minimum_length_encoding(lists[r % count])
        total += answer
        checksum = (checksum * 131 + answer) % 1000000007
    print(f"{rounds} rounds of {count} lists of 2000 words: total {total}, checksum {checksum}")


main()

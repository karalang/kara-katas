# Benchmark for #676: every word of the same length compared, as the
# Kara ★ arm.


class MagicDictionary:
    def __init__(self):
        self.words = []

    def build_dict(self, dictionary):
        self.words = list(dictionary)

    def search(self, search_word):
        b = search_word.encode()
        for w in self.words:
            a = w.encode()
            if len(a) == len(b):
                diff = 0
                for i in range(len(a)):
                    if a[i] != b[i]:
                        diff += 1
                if diff == 1:
                    return True
        return False


seed = 676


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length):
    return "".join(chr(97 + next_random() % 2) for _ in range(length))


def main():
    rounds = 1000
    s = 0
    found = 0
    for _ in range(rounds):
        dictionary = [random_word(50) for _ in range(100)]
        d = MagicDictionary()
        d.build_dict(dictionary)
        for k in range(100):
            if k % 2 == 0:
                w = dictionary[next_random() % 100]
                at = next_random() % 50
                c = "b" if w[at] == "a" else "a"
                word = w[:at] + c + w[at + 1:]
            else:
                word = random_word(50)
            if d.search(word):
                found += 1
                s = (s * 3 + 1) % 1000000007
            else:
                s = s * 3 % 1000000007
    print(f"{rounds} dictionaries of 100 words, {rounds * 100} searches, {found} found: checksum {s}")


main()

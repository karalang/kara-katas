# LeetCode #676: Implement Magic Dictionary -- every word of the same
# length compared.
# Mirrors the ★ arm (magic_dictionary.kara) and its test harness.


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


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def run_all(dictionary, searches):
    d = MagicDictionary()
    d.build_dict(dictionary)
    out = ["null", "null"]
    for w in searches:
        out.append("true" if d.search(w) else "false")
    return "[" + ",".join(out) + "]"


def random_word(rng, most, letters):
    n = 1 + rng.next() % most
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def main():
    print(run_all(["hello", "leetcode"], ["hello", "hhllo", "hell", "leetcoded"]))
    print(run_all(["a"], ["a", "b", "aa", "z"]))
    print(run_all(["ab", "ba"], ["aa", "bb", "ab", "ba", "cb"]))
    print(run_all(["hello", "hallo"], ["hello", "hallo", "hullo", "hxllx"]))
    print(run_all(["abc", "abd", "xyz"], ["abc", "abz", "xbz", "ayz", "xyzz"]))
    print(run_all(["a" * 100], ["a" * 99 + "b", "b" + "a" * 99, "a" * 100, "a" * 101]))
    rng = Rng(676)
    s = 0
    hits = 0
    total = 0
    for c in range(300):
        letters = 2 + c % 3
        most = 1 + c % 6
        dictionary = []
        for _ in range(1 + rng.next() % 30):
            w = random_word(rng, most, letters)
            if w not in dictionary:
                dictionary.append(w)
        d = MagicDictionary()
        d.build_dict(dictionary)
        for _ in range(20):
            got = d.search(random_word(rng, most, letters))
            total += 1
            if got:
                hits += 1
            s = (s * 3 + (1 if got else 0)) % 1000000007
    print(f"{total} random searches: {hits} true, checksum {s}")


main()

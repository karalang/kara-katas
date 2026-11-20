# LeetCode #1286: Iterator for Combination -- Python mirror of the ★ arm:
# the masks with k bits, from the largest down.


class CombinationIterator:
    def __init__(self, characters, combination_length):
        n = len(characters)
        self.chars = list(characters)
        self.k = combination_length
        self.mask = ((1 << combination_length) - 1) << (n - combination_length)

    def next(self):
        n = len(self.chars)
        out = "".join(self.chars[i] for i in range(n) if (self.mask >> (n - 1 - i)) & 1)
        self.mask -= 1
        while self.mask > 0 and bin(self.mask).count("1") != self.k:
            self.mask -= 1
        return out

    def has_next(self):
        return self.mask > 0


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(n):
    out = ""
    left = n
    for i, c in enumerate("abcdefghijklmnopqrstuvwxyz"):
        if left > 0 and next_random() % (26 - i) < left:
            out += c
            left -= 1
    return out


def main():
    global seed
    it = CombinationIterator("abc", 2)
    first = it.next()
    a = it.has_next()
    second = it.next()
    b = it.has_next()
    third = it.next()
    c = it.has_next()
    t = lambda v: "true" if v else "false"
    print(f"{first} {t(a)} {second} {t(b)} {third} {t(c)}")
    seed = 1286
    check = 0
    for n in range(1, 16):
        count = 0
        last = ""
        for k in range(1, n + 1):
            it = CombinationIterator(letters(n), k)
            while it.has_next():
                if next_random() % 3 == 0:
                    if not it.has_next():
                        print("has_next changed its answer")
                s = it.next()
                count += 1
                for b in s.encode():
                    check = (check * 131 + b) % 1000000007
                check = (check * 131 + 7) % 1000000007
                last = s
        print(f"{n} letters: {count} combinations, the last {last}")
    print(f"checksum {check}")


if __name__ == "__main__":
    main()

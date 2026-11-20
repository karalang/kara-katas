# LeetCode #1286 bench, in Python: the ★ arm (the masks with k bits, from
# the largest down) over every length of 15 letters, 1000 rounds.


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


def main():
    check = 0
    for rnd in range(1000):
        for k in range(1, 16):
            it = CombinationIterator("abcdefghijklmno", k)
            while it.has_next():
                for b in it.next().encode():
                    check = (check * 131 + b + rnd) % 1000000007
    print(f"1000 rounds of every length of 15 letters: checksum {check}")


if __name__ == "__main__":
    main()

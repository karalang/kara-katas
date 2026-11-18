"""LeetCode #1618: Maximum Font to Fit a Sentence in a Screen -- Python mirror
of the ★ arm (fonts.kara): a binary search for the last size that fits."""


class Font:
    def __init__(self, base):
        self.base = base

    def get_width(self, font_size, ch):
        return (font_size * self.base[ord(ch) - ord("a")] + 3) // 4

    def get_height(self, font_size):
        return font_size + font_size // 4


def fits(text, w, h, size, info):
    return info.get_height(size) <= h and sum(info.get_width(size, c) for c in text) <= w


def max_font(text, w, h, fonts, info):
    lo, hi = 0, len(fonts)
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(text, w, h, fonts[mid], info):
            lo = mid + 1
        else:
            hi = mid
    return -1 if lo == 0 else fonts[lo - 1]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self, bound):
        return (self.next() * 32768 + self.next()) % bound


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, rng):
    check = fits_n = letters = 0
    for _ in range(count):
        font = Font([rng.next() % 8 + 1 for _ in range(26)])
        n = rng.wide(most) + 1
        text = "".join(chr(ord("a") + rng.next() % 26) for _ in range(n))
        fonts = []
        size = 0
        for _ in range(rng.next() % 20 + 1):
            size += rng.next() % 30 + 1
            fonts.append(size)
        w = rng.wide(n * 40) + 1
        h = rng.next() % 400 + 1
        answer = max_font(text, w, h, fonts, font)
        if answer >= 0:
            fits_n += 1
        check = mix(check, answer)
        letters += n
    print(f"{count} screens for up to {most} letters: {letters} letters, {fits_n} fit, checksum {check}")


def main():
    plain = Font([4] * 26)
    print(max_font("helloworld", 80, 20, [6, 8, 10, 12, 14, 16, 18, 24, 36], plain))
    print(max_font("leetcode", 1000, 50, [1, 2, 4], plain))
    print(max_font("easyquestion", 100, 100, [10, 15, 20, 25], plain))
    rng = Rng(1618)
    batch(3000, 10, rng)
    batch(300, 1000, rng)
    batch(30, 50000, rng)


main()

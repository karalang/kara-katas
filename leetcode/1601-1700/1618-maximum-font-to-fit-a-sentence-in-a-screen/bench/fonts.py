"""LeetCode #1618: Maximum Font to Fit a Sentence in a Screen -- the bench in
Python, mirroring fonts.kara: a binary search for the last size that fits."""


class Font:
    def __init__(self, base):
        self.base = base

    def get_width(self, font_size, ch):
        return (font_size * self.base[ord(ch) - 97] + 3) // 4

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


def main():
    seed = 1618

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    texts = ["".join(chr(97 + next_random() % 26) for _ in range(5000)) for _ in range(200)]
    font = Font([next_random() % 8 + 1 for _ in range(26)])
    fonts = [k * 3 for k in range(1, 61)]
    check = total = 0
    for text in texts:
        for _ in range(40):
            w = next_random() * 8 + 1
            h = next_random() % 240 + 1
            answer = max_font(text, w, h, fonts, font)
            check = (check * 31 + answer + 1) % 1000000007
            total += answer
    print(f"8000 screens of 5000 letters: sizes total {total}, checksum {check}")


main()

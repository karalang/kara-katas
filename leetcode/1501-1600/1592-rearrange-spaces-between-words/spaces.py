# LeetCode #1592: Rearrange Spaces Between Words -- the Python mirror of
# spaces.kara: the words by split(), the spaces counted and shared out.


def reorder_spaces(text):
    words = text.split()
    spaces = text.count(" ")
    gaps = len(words) - 1
    if gaps == 0:
        return words[0] + " " * spaces
    return (" " * (spaces // gaps)).join(words) + " " * (spaces % gaps)


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def wide(self):
        a = self.next()
        return a * 32768 + self.next()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def draw(n, rng):
    b = []
    for _ in range(n):
        r = rng.next() % 6
        b.append(" " if r < 2 else chr(ord("a") + (r - 2) % 3))
    at = rng.wide() % n
    b[at] = "a"
    return "".join(b)


def batch(count, most, rng):
    check = 0
    trailing = 0
    for _ in range(count):
        n = rng.wide() % most + 1
        answer = reorder_spaces(draw(n, rng))
        if answer.endswith(" "):
            trailing += 1
        for c in answer.encode():
            check = mix(check, c)
    print(f"{count} texts of up to {most} characters: {trailing} end in a space, checksum {check}")


def main():
    examples = ["  this   is  a sentence ", " practice   makes   perfect", "hello", "  hello  ", "a b", "a  b c", " a", "x y z  "]
    for text in examples:
        print(f'"{text}" -> "{reorder_spaces(text)}"')
    rng = Rng(1592)
    batch(3000, 10, rng)
    batch(300, 100, rng)
    batch(10, 100000, rng)


main()

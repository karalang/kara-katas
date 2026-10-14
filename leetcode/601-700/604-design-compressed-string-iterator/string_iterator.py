# LeetCode #604: Design Compressed String Iterator -- read as you go.
#
# Mirrors string_iterator.kara: the next letter and its count are read
# from the text only when the one in hand runs out.


class StringIterator:
    def __init__(self, compressed):
        self.text = list(compressed)
        self.at = 0
        self.current = ' '
        self.left = 0

    def next(self):
        if self.left == 0:
            if self.at == len(self.text):
                return ' '
            self.current = self.text[self.at]
            self.at += 1
            count = 0
            while self.at < len(self.text) and self.text[self.at].isdigit():
                count = count * 10 + (ord(self.text[self.at]) - 48)
                self.at += 1
            self.left = count
        self.left -= 1
        return self.current

    def has_next(self):
        return self.left > 0 or self.at < len(self.text)


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def run(compressed, ops):
    it = StringIterator(compressed)
    out = []
    for op in ops:
        if op == 'n':
            c = it.next()
            out.append("_" if c == ' ' else c)
        else:
            out.append("true" if it.has_next() else "false")
    return out


def text(items):
    return "[" + ", ".join(items) + "]"


def show(compressed, ops):
    print(f"{compressed} {ops} -> {text(run(compressed, ops))}")


def main():
    show("L1e2t1C1o1d1e1", "nnnnnnhnh")
    show("a2b1", "hnnhnhnn")
    show("Q1", "hnhnh")
    show("a12B3", "nnnnnnnnnnnnnnnhn")
    show("x10y1", "nnnnnnnnnnnhnh")
    show("k100", "hnhnhnh")
    show("a1A1a1", "nnnnh")
    got = run("z1000000000", "n" * 99 + "h")
    print(f"z1000000000, 99 next then has_next -> {len(got)} results, the last {got[98]} {got[99]}")
    alphabet = "".join(chr(97 + k) + "1" for k in range(26))
    print(f"a1b1...z1 and past the end -> {text(run(alphabet, 'nnnnnnnnnnnnnnnnnnnnnnnnnnnhnh'))}")
    seed = [604]
    total = 0
    checksum = 0
    for _ in range(300):
        parts = []
        runs = 1 + step(seed) % 12
        for _ in range(runs):
            k = step(seed) % 52
            parts.append(chr(65 + k) if k < 26 else chr(97 + k - 26))
            if step(seed) % 10 == 0:
                hi = step(seed)
                lo = step(seed)
                count = 1 + (hi * 32768 + lo) % 1000000000
            else:
                count = 1 + step(seed) % 20
            parts.append(str(count))
        size = 1 + step(seed) % 100
        calls = "".join('h' if step(seed) % 3 == 0 else 'n' for _ in range(size))
        for r in run("".join(parts), calls):
            total += 1
            for c in r:
                checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"300 random cases: {total} results, checksum {checksum}")


main()

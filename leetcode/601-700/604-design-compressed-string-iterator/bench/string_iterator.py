# Benchmark for #604: Python mirror of the ★ arm (read as you go); see
# string_iterator.kara.


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


# ---- benchmark ----------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 1000
    rounds = 200
    seed = [604]
    texts = []
    for _ in range(count):
        text = ""
        while True:
            k = step(seed) % 52
            letter = chr(65 + k) if k < 26 else chr(97 + k - 26)
            if step(seed) % 10 == 0:
                hi = step(seed)
                lo = step(seed)
                n = 1 + (hi * 32768 + lo) % 1000000000
            else:
                n = 1 + step(seed) % 20
            run = f"{letter}{n}"
            if len(text) + len(run) > 1000:
                break
            text += run
        texts.append(text)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            it = StringIterator(texts[(rnd * 7 + g) % count])
            for _ in range(50):
                if it.has_next():
                    total += 1
                c = it.next()
                checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"{count} texts, {rounds} rounds: {total} letters left, checksum {checksum}")


main()

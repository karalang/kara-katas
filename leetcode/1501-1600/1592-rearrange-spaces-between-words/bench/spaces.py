# LeetCode #1592: Rearrange Spaces Between Words -- the bench in Python,
# mirroring spaces.kara.


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


def draw(n, rng):
    b = []
    for _ in range(n):
        r = rng.next() % 6
        b.append(" " if r < 2 else chr(ord("a") + (r - 2) % 3))
    at = rng.wide() % n
    b[at] = "a"
    return "".join(b)


def main():
    rng = Rng(1592)
    texts = [draw(100000, rng) for _ in range(200)]
    check = 0
    trailing = 0
    for text in texts:
        answer = reorder_spaces(text)
        trailing += len(answer) - len(answer.rstrip(" "))
        for c in answer.encode():
            check = (check * 31 + c + 1) % 1000000007
    print(f"200 texts of 100000 characters: {trailing} trailing spaces, checksum {check}")


main()

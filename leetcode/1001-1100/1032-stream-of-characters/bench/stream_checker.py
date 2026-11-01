# LeetCode #1032: Stream of Characters -- bench
# Mirrors ./stream_checker.kara; see ../README.md § Benchmarks.


class StreamChecker:
    def __init__(self, words):
        self.next = [[-1] * 26]
        self.end = [False]
        for word in words:
            node = 0
            for c in reversed(word):
                k = ord(c) - ord('a')
                if self.next[node][k] == -1:
                    self.next[node][k] = len(self.next)
                    self.next.append([-1] * 26)
                    self.end.append(False)
                node = self.next[node][k]
            self.end[node] = True
        self.stream = []

    def query(self, letter):
        self.stream.append(ord(letter) - ord('a'))
        node = 0
        i = len(self.stream)
        while i > 0:
            i -= 1
            node = self.next[node][self.stream[i]]
            if node == -1:
                return False
            if self.end[node]:
                return True
        return False


seed = 1032


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(length):
    return "".join(chr(97 + next_random() % 2) for _ in range(length))


def main():
    rounds = 50
    words = []
    for _ in range(2000):
        length = 50 + next_random() % 151
        words.append(random_text(length))
    stream = random_text(40000)
    found = 0
    check = 0
    for _ in range(rounds):
        checker = StreamChecker(list(words))
        for c in stream:
            hit = 1 if checker.query(c) else 0
            found += hit
            check = (check * 3 + hit + 1) % 1000000007
    print(f"2000 words, 40000 queries, {rounds} rounds: {found} found, checksum {check}")


main()

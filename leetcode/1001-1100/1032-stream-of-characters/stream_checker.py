# LeetCode #1032: Stream of Characters -- a trie of the reversed words
# Mirrors stream_checker.kara (the ★ arm) and prints the same output.


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


def answers(words, stream):
    checker = StreamChecker(list(words))
    return "".join("T" if checker.query(c) else "F" for c in stream)


def random_text(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    examples = [
        (["cd", "f", "kl"], "abcdefghijkl"),
        (["ab", "ba", "aaab", "abab", "baa"], "aaaaabababbbababbbbababaaabaaa"),
        (["a"], "abcaba"),
        (["abc", "bc", "c"], "abcbcc"),
        (["aaa"], "aaaaaa"),
        (["zz", "xyz"], "xyzzyxz"),
    ]
    for words, stream in examples:
        print(f"{','.join(words)} / {stream}: {answers(words, stream)}")
    groups = [
        (1000, 3, 3, 2, 30), (300, 10, 6, 3, 200), (100, 40, 12, 4, 500),
        (20, 200, 40, 6, 2000), (5, 100, 5, 26, 4000), (2, 2000, 200, 26, 20000),
    ]
    for count, word_count, longest, letters, queries in groups:
        found = 0
        check = 0
        for _ in range(count):
            words = []
            for _ in range(word_count):
                length = next_random() % longest + 1
                words.append(random_text(length, letters))
            stream = random_text(queries, letters)
            for c in answers(words, stream):
                hit = 1 if c == "T" else 0
                found += hit
                check = (check * 3 + hit + 1) % 1000000007
        print(f"{count} checkers of {word_count} words up to {longest} letters over {letters}, "
              f"{queries} queries each: {found} found, checksum {check}")
    many_a = "a" * 40000
    long_a = "a" * 200
    ones = answers(["a"], many_a)
    longs = answers([long_a, "b"], many_a)
    print(f"\"a\" against 40000 a's: {ones.count('T')} found")
    print(f"200 a's and \"b\" against 40000 a's: {longs.count('T')} found, first at query {longs.find('T') + 1}")


main()

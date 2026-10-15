# Benchmark for #642: mirror of autocomplete.kara (the ★ arm: a trie
# searched below the prefix) on the same workload.
import sys


def branch(c):
    return 26 if c == " " else ord(c) - ord("a")


def letter(b):
    return " " if b == 26 else chr(ord("a") + b)


class Node:
    __slots__ = ("children", "count")

    def __init__(self):
        self.children = [-1] * 27
        self.count = 0


def gather(nodes, node, path, found):
    n = nodes[node]
    if n.count > 0:
        found.append((n.count, path))
    for b in range(27):
        child = n.children[b]
        if child != -1:
            gather(nodes, child, path + letter(b), found)


class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.nodes = [Node()]
        self.typed = ""
        self.at = 0
        for s, t in zip(sentences, times):
            self.add(s, t)

    def add(self, sentence, times):
        node = 0
        for c in sentence:
            b = branch(c)
            if self.nodes[node].children[b] == -1:
                self.nodes.append(Node())
                self.nodes[node].children[b] = len(self.nodes) - 1
            node = self.nodes[node].children[b]
        self.nodes[node].count += times

    def input(self, c):
        if c == "#":
            self.add(self.typed, 1)
            self.typed = ""
            self.at = 0
            return []
        self.typed += c
        if self.at != -1:
            self.at = self.nodes[self.at].children[branch(c)]
        if self.at == -1:
            return []
        found = []
        gather(self.nodes, self.at, self.typed, found)
        found.sort(key=lambda e: (-e[0], e[1]))
        return [s for _, s in found[:3]]


class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_sentence(most, rng):
    length = 1 + rng.next() % most
    return "".join("abc "[rng.next() % 4] for _ in range(length))


def main():
    rng = Random(642)
    histories = []
    for _ in range(10):
        sentences = []
        times = []
        while len(sentences) < 100:
            s = random_sentence(100, rng)
            if s not in sentences:
                sentences.append(s)
                times.append(1 + rng.next() % 100)
        typing = ""
        while len(typing) < 5000:
            if rng.next() % 2 == 0:
                typing += sentences[rng.next() % 100]
            else:
                typing += random_sentence(100, rng)
            typing += "#"
        histories.append((sentences, times, typing[:5000]))
    rounds = 40
    names = 0
    checksum = 0
    for r in range(rounds):
        sentences, times, typing = histories[r % 10]
        system = AutocompleteSystem(sentences, times)
        for c in typing:
            for name in system.input(c):
                checksum = (checksum * 31 + len(name) * 65536 + ord(name[0]) * 256 + ord(name[-1])) % 1000000007
                names += 1
            checksum = (checksum * 31 + 1) % 1000000007
    print(f"{rounds} rounds of 5000 calls: {names} names, checksum {checksum}")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()

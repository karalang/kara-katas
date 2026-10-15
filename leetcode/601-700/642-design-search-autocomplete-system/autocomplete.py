# LeetCode #642: Design Search Autocomplete System -- Python mirror of the
# ★ arm.
#
# A trie of 27 branches, each sentence's end keeping its count; each call
# gathers everything below the typed prefix and keeps the three hottest.


def branch(c):
    return 26 if c == " " else ord(c) - ord("a")


def letter(b):
    return " " if b == 26 else chr(ord("a") + b)


class Node:
    def __init__(self):
        self.children = [-1] * 27
        self.count = 0


def gather(nodes, node, path, found):
    if nodes[node].count > 0:
        found.append((nodes[node].count, path))
    for b in range(27):
        child = nodes[node].children[b]
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


# ---- test harness ----------------------------------------------------------

class Random:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def run_all(sentences, times, typing):
    system = AutocompleteSystem(sentences, times)
    out = "[null"
    for c in typing:
        got = system.input(c)
        out += ",[" + ",".join('"' + s + '"' for s in got) + "]"
    return out + "]"


def show(sentences, times, typing):
    print(run_all(sentences, times, typing))


def words(text):
    return text.split(",")


def random_sentence(most, alphabet, rng):
    length = 1 + rng.next() % most
    s = ""
    for _ in range(length):
        i = rng.next() % len(alphabet)
        s += alphabet[i]
    return s


def random_case(n, most, alphabet, hottest, calls, rng):
    sentences = []
    times = []
    while len(sentences) < n:
        s = random_sentence(most, alphabet, rng)
        if s not in sentences:
            sentences.append(s)
            times.append(1 + rng.next() % hottest)
    typing = ""
    while len(typing) < calls:
        if n > 0 and rng.next() % 2 == 0:
            typing += sentences[rng.next() % n]
        else:
            typing += random_sentence(most, alphabet, rng)
        typing += "#"
    return sentences, times, typing[:calls]


def summary(s):
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % 1000000007
    return f"{len(s)} characters, checksum {h}"


def main():
    show(words("i love you,island,iroman,i love leetcode"), [5, 3, 2, 2], "i a#")
    show(words("ab,a b,a,abc"), [1, 1, 1, 1], "a#")
    show(words("hello,help"), [2, 2], "hel#hel#hel#he")
    show([], [], "ab#a#ab#a")
    show(words("cat,car"), [1, 1], "cx#cx#c")
    show(words("go,gone,goal,good,got"), [4, 3, 5, 1, 3], "go#go")
    show(words("a,aa,aaa"), [3, 2, 1], "aa#aaa#aaa#a")
    rng = Random(642)
    total = ""
    for _ in range(300):
        n = rng.next() % 8
        calls = 1 + rng.next() % 40
        sentences, times, typing = random_case(n, 6, "ab ", 5, calls, rng)
        total += run_all(sentences, times, typing)
    print(f"300 random systems: {summary(total)}")
    sentences, times, typing = random_case(100, 100, "abc ", 100, 5000, rng)
    print(f"100 sentences, 5000 calls: {summary(run_all(sentences, times, typing))}")


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)
    main()

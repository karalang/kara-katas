# LeetCode #1258 bench, in Python: the ★ arm (union-find over the pairs'
# words, the groups sorted, every sentence built by a recursive search, the
# sentences sorted) on 100 random cases built once, each 10 pairs of 8
# words and a text of 10 words, 4 of them from the pairs, asked 80 rounds;
# the sentences counted and the middle one of each answer folded into a
# checksum.


def find(parent, word):
    up = parent[word]
    if up == word:
        return up
    root = find(parent, up)
    parent[word] = root
    return root


def build(choices, at, current, out):
    if at == len(choices):
        out.append(" ".join(current))
        return
    for word in choices[at]:
        current.append(word)
        build(choices, at + 1, current, out)
        current.pop()


def generate_sentences(synonyms, text):
    parent = {}
    for pair in synonyms:
        for word in pair:
            if word not in parent:
                parent[word] = word
    for a, b in synonyms:
        a, b = find(parent, a), find(parent, b)
        if a != b:
            parent[a] = b
    groups = {}
    for word in list(parent):
        groups.setdefault(find(parent, word), []).append(word)
    choices = []
    for word in text.split(" "):
        if word in parent:
            choices.append(sorted(groups[find(parent, word)]))
        else:
            choices.append([word])
    out = []
    build(choices, 0, [], out)
    out.sort()
    return out


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_word(first, rng):
    n = rng.next() % 3 + 1
    return "".join(chr(first + rng.next() % 6) for _ in range(n))


def random_words(count, first, rng):
    words = []
    while len(words) < count:
        w = random_word(first, rng)
        if w not in words:
            words.append(w)
    return words


def bench_case(rng):
    pool = random_words(8, ord("a"), rng)
    plain = random_words(12, ord("p"), rng)
    synonyms = []
    for _ in range(10):
        i = rng.next() % 8
        j = (i + 1 + rng.next() % 7) % 8
        synonyms.append([pool[i], pool[j]])
    words = [plain[rng.next() % 12] for _ in range(10)]
    for k in range(4):
        words[k * 3] = pool[rng.next() % 8]
    return synonyms, " ".join(words)


def main():
    rng = Rng(1258)
    cases = [bench_case(rng) for _ in range(100)]
    total = 0
    check = 0
    for _ in range(80):
        for synonyms, text in cases:
            sentences = generate_sentences(synonyms, text)
            total += len(sentences)
            for b in sentences[len(sentences) // 2].encode():
                check = (check * 131 + b) % 1000000007
    print(f"80 rounds of 100 cases: {total} sentences, checksum {check}")


main()

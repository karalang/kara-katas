# LeetCode #1258: Synonymous Sentences -- Python mirror of the ★ arm
# (union-find over the pairs' words, the groups sorted, every sentence built
# by a recursive search, the sentences sorted), with the same harness.


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


def random_case(rng):
    pool = random_words(8, ord("a"), rng)
    plain = random_words(12, ord("p"), rng)
    synonyms = []
    for _ in range(rng.next() % 11):
        i = rng.next() % 8
        j = (i + 1 + rng.next() % 7) % 8
        synonyms.append([pool[i], pool[j]])
    words = []
    from_pool = 0
    for _ in range(rng.next() % 10 + 1):
        if from_pool < 4 and rng.next() % 3 == 0:
            words.append(pool[rng.next() % 8])
            from_pool += 1
        else:
            words.append(plain[rng.next() % 12])
    return synonyms, " ".join(words)


def fold(check, sentence):
    for b in sentence.encode():
        check = (check * 131 + b) % 1000000007
    return (check * 131 + 10) % 1000000007


def main():
    text = "I am happy today but was sad yesterday"
    for s in generate_sentences([["happy", "joy"], ["sad", "sorrow"], ["joy", "cheerful"]], text):
        print(s)
    second = generate_sentences([["happy", "joy"], ["cheerful", "glad"]], text)
    print(f"{len(second)} sentences: {' / '.join(second)}")
    rng = Rng(1258)
    total = 0
    check = 0
    for _ in range(400):
        synonyms, text = random_case(rng)
        sentences = generate_sentences(synonyms, text)
        total += len(sentences)
        for s in sentences:
            check = fold(check, s)
    print(f"400 random cases: {total} sentences, checksum {check}")
    top = []
    for i in range(5):
        top.append([f"joy{i}", f"joy{i + 1}"])
        top.append([f"sad{5 - i}", f"sad{4 - i}"])
    many = generate_sentences(top, "joy3 was not sad2 but joy0 and sad5 for days")
    check = 0
    for s in many:
        check = fold(check, s)
    print(f"{len(many)} sentences, checksum {check}, first {many[0]}, last {many[-1]}")


main()

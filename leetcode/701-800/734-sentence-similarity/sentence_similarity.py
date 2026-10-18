# LeetCode #734: Sentence Similarity -- mirror of the star arm.


def are_sentences_similar(sentence1, sentence2, pairs):
    if len(sentence1) != len(sentence2):
        return False
    similar = set()
    for a, b in pairs:
        similar.add((a, b))
        similar.add((b, a))
    for a, b in zip(sentence1, sentence2):
        if a != b and (a, b) not in similar:
            return False
    return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def words(text):
    return [w for w in text.split(" ") if w]


def pairs_of(text):
    w = words(text)
    return [(w[i], w[i + 1]) for i in range(0, len(w) - 1, 2)]


def b(v):
    return "true" if v else "false"


def fmt_words(ws):
    return "[" + ", ".join(ws) + "]"


def fmt_pairs(ps):
    return "[" + ", ".join(f"({x}, {y})" for x, y in ps) + "]"


def show(a, c, p):
    s1, s2, pairs = words(a), words(c), pairs_of(p)
    print(f"{fmt_words(s1)} and {fmt_words(s2)} with {fmt_pairs(pairs)} -> {b(are_sentences_similar(s1, s2, pairs))}")


def word(k):
    return f"w{k}"


def main():
    global seed
    show("great acting skills", "fine drama talent", "great fine drama acting skills talent")
    show("great", "great", "")
    show("great", "doubleplus good", "great doubleplus")
    show("a", "c", "a b b c")
    show("b", "a", "a b")
    show("a b", "b a", "a b")
    show("x y z", "x y q", "x q y q")
    seed = 734
    pairs = []
    for _ in range(1000):
        x = word(next_random() % 200)
        pairs.append((x, word(next_random() % 200)))
    s1, s2 = [], []
    for _ in range(1000):
        p = pairs[next_random() % 1000]
        if next_random() % 2 == 0:
            s1.append(p[0])
            s2.append(p[1])
        else:
            s1.append(p[1])
            s2.append(p[0])
    print(f"1000 words, each paired with its counterpart -> {b(are_sentences_similar(s1, s2, pairs))}")
    changed = s2[:]
    changed[999] = "nowhere"
    print(f"the same with the last word changed -> {b(are_sentences_similar(s1, changed, pairs))}")
    print(f"the same with the pairs left out -> {b(are_sentences_similar(s1, s2, []))}")
    print(f"the same one word short -> {b(are_sentences_similar(s1, s2[:-1], pairs))}")
    yes = 0
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 6
        np_ = next_random() % 7
        ps = []
        for _ in range(np_):
            x = word(next_random() % 6)
            ps.append((x, word(next_random() % 6)))
        a, c = [], []
        for _ in range(n):
            x = next_random() % 6
            a.append(word(x))
            pick = next_random() % 3
            if pick == 0 or np_ == 0:
                c.append(word(x))
            elif pick == 1:
                c.append(ps[next_random() % np_][1])
            else:
                c.append(word(next_random() % 6))
        if next_random() % 10 == 0:
            c.append(word(0))
        v = 1 if are_sentences_similar(a, c, ps) else 0
        yes += v
        total = (total * 131 + v + 1) % 1000000007
    print(f"300 random cases: {yes} similar, checksum {total}")


main()

# LeetCode #737: Sentence Similarity II -- union-find.
# Mirror of the Kara star arm: number every word in a pair, join the two
# words of each pair in a union-find with union by size and path
# compression, and compare the roots of the two words at each place.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def number(ids, parent, size, w):
    if w in ids:
        return ids[w]
    i = len(parent)
    ids[w] = i
    parent.append(i)
    size.append(1)
    return i


def are_sentences_similar_two(sentence1, sentence2, pairs):
    if len(sentence1) != len(sentence2):
        return False
    ids, parent, size = {}, [], []
    for p0, p1 in pairs:
        a = number(ids, parent, size, p0)
        b = number(ids, parent, size, p1)
        ra, rb = find(parent, a), find(parent, b)
        if ra != rb:
            if size[ra] < size[rb]:
                parent[ra] = rb
                size[rb] += size[ra]
            else:
                parent[rb] = ra
                size[ra] += size[rb]
    for w1, w2 in zip(sentence1, sentence2):
        if w1 == w2:
            continue
        if w1 not in ids or w2 not in ids:
            return False
        if find(parent, ids[w1]) != find(parent, ids[w2]):
            return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def words(text):
    return [w for w in text.split(" ") if w]


def pairs_of(text):
    w = words(text)
    return [(w[i], w[i + 1]) for i in range(0, len(w) - 1, 2)]


def show_list(xs):
    return "[" + ", ".join(xs) + "]"


def show_pairs(ps):
    return "[" + ", ".join(f"({a}, {b})" for a, b in ps) + "]"


def show(a, b, p):
    s1, s2, pairs = words(a), words(b), pairs_of(p)
    r = "true" if are_sentences_similar_two(s1, s2, pairs) else "false"
    print(f"{show_list(s1)} and {show_list(s2)} with {show_pairs(pairs)} -> {r}")


def tf(v):
    return "true" if v else "false"


def word(k):
    return f"w{k}"


def main():
    show("great acting skills", "fine drama talent", "great good fine good drama acting skills talent")
    show("I love leetcode", "I love onepiece", "manga onepiece platform anime leetcode platform anime manga")
    show("I love leetcode", "I love onepiece", "manga hunterXhunter platform anime leetcode platform anime manga")
    show("a", "c", "a b b c")
    show("a", "c", "a b c d")
    show("great", "great", "")
    show("great", "doubleplus good", "great doubleplus")
    show("x y", "y x", "x z z y")
    seed = [737]
    chain = [(word(k), word(k + 1)) for k in range(999)]
    for k in range(999):
        j = k + next_random(seed) % (999 - k)
        chain[k], chain[j] = chain[j], chain[k]
    print(f"the two ends of a chain of 1000 words -> {tf(are_sentences_similar_two([word(0)], [word(999)], chain))}")
    del chain[500]
    print(f"the same with one pair of the chain left out -> {tf(are_sentences_similar_two([word(0)], [word(999)], chain))}")
    pairs = []
    near = [[] for _ in range(3000)]
    for _ in range(2000):
        a = next_random(seed) % 3000
        b = next_random(seed) % 3000
        pairs.append((word(a), word(b)))
        near[a].append(b)
        near[b].append(a)
    s1, s2 = [], []
    for _ in range(1000):
        start = next_random(seed) % 3000
        at = start
        for _ in range(next_random(seed) % 6):
            if near[at]:
                at = near[at][next_random(seed) % len(near[at])]
        s1.append(word(start))
        s2.append(word(at))
    print(f"1000 words, each joined to its counterpart by up to 5 pairs -> {tf(are_sentences_similar_two(s1, s2, pairs))}")
    changed = list(s2)
    changed[999] = "nowhere"
    print(f"the same with the last word changed -> {tf(are_sentences_similar_two(s1, changed, pairs))}")
    print(f"the same with the pairs left out -> {tf(are_sentences_similar_two(s1, s2, []))}")
    print(f"the same one word short -> {tf(are_sentences_similar_two(s1, s2[:-1], pairs))}")
    yes = 0
    total = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 6
        np_ = next_random(seed) % 7
        ps = []
        for _ in range(np_):
            ps.append((word(next_random(seed) % 8), word(next_random(seed) % 8)))
        a, b = [], []
        for _ in range(n):
            x = next_random(seed) % 8
            a.append(word(x))
            pick = next_random(seed) % 3
            if pick == 0 or np_ == 0:
                b.append(word(x))
            elif pick == 1:
                p = next_random(seed) % np_
                if next_random(seed) % 2 == 0:
                    b.append(ps[p][0])
                else:
                    b.append(ps[p][1])
            else:
                b.append(word(next_random(seed) % 8))
        if next_random(seed) % 10 == 0:
            b.append(word(0))
        v = 1 if are_sentences_similar_two(a, b, ps) else 0
        yes += v
        total = (total * 131 + v + 1) % 1000000007
    print(f"300 random cases: {yes} similar, checksum {total}")


main()

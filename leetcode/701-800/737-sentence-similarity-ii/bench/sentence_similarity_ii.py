# LeetCode #737: Sentence Similarity II -- union-find.
# Benchmark mirror of the Kara star arm: number every word in a pair,
# join the two words of each pair in a union-find with union by size
# and path compression, and compare the roots of the two words at each
# place.


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



def main():
    seed = [737]
    pairs = []
    near = [[] for _ in range(3000)]
    for _ in range(2000):
        a = next_random(seed) % 3000
        b = next_random(seed) % 3000
        pairs.append((f"w{a}", f"w{b}"))
        near[a].append(b)
        near[b].append(a)
    s1, s2 = [], []
    for _ in range(1000):
        start = next_random(seed) % 3000
        at = start
        for _ in range(next_random(seed) % 6):
            if near[at]:
                at = near[at][next_random(seed) % len(near[at])]
        s1.append(f"w{start}")
        s2.append(f"w{at}")
    similar = 0
    for _ in range(1000):
        j = next_random(seed) % 1000
        x = next_random(seed) % 3000
        saved = s2[j]
        s2[j] = f"w{x}"
        if are_sentences_similar_two(s1, s2, pairs):
            similar += 1
        s2[j] = saved
        if are_sentences_similar_two(s1, s2, pairs):
            similar += 1
    print(f"1000 rounds of 2 checks of 1000 words with 2000 pairs: {similar} similar")


main()

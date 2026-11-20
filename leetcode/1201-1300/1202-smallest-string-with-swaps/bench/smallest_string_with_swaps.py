# LeetCode #1202 bench, in Python: the ★ arm (a union-find over the
# indices, path halving and union by size; each group's letters, sorted, go
# back to its indices in rising order) on one string of 100000 random
# letters and four sets of pairs drawn once, then 10 rounds over the four,
# each answer folded into a checksum.

seed = 1202


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def smallest_string_with_swaps(s, pairs):
    n = len(s)
    parent = list(range(n))
    size = [1] * n
    for p in pairs:
        a = find(parent, p[0])
        b = find(parent, p[1])
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
    groups = [[] for _ in range(n)]
    for i in range(n):
        groups[find(parent, i)].append(i)
    out = bytearray(s)
    for g in groups:
        letters = sorted(s[i] for i in g)
        for k in range(len(g)):
            out[g[k]] = letters[k]
    return bytes(out)


def random_pairs(n, m):
    pairs = []
    for _ in range(m):
        a = (next_random() * 32768 + next_random()) % n
        b = (next_random() * 32768 + next_random()) % n
        pairs.append([a, b])
    return pairs


def main():
    n = 100000
    s = bytes(ord("a") + next_random() % 26 for _ in range(n))
    sets = [
        random_pairs(n, 25000),
        random_pairs(n, 100000),
        [[i, i + 2] for i in range(n - 2)],
        [[i, i + 1000] for i in range(n - 1000)],
    ]
    check = 0
    for _ in range(10):
        for pairs in sets:
            t = smallest_string_with_swaps(s, pairs)
            for b in t:
                check = (check * 131 + b) % 1000000007
    print(f"10 rounds over 4 sets of pairs on 100000 letters: checksum {check}")


main()

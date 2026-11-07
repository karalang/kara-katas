# LeetCode #1061: Lexicographically Smallest Equivalent String -- the
# benchmark, the same union-find as lexi.kara.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    y = x
    while parent[y] != root:
        nxt = parent[y]
        parent[y] = root
        y = nxt
    return root


def smallest_equivalent(s1, s2, base):
    parent = list(range(26))
    for a, b in zip(s1, s2):
        ra = find(parent, a - 97)
        rb = find(parent, b - 97)
        if ra < rb:
            parent[rb] = ra
        else:
            parent[ra] = rb
    out = bytearray()
    for c in base:
        out.append(97 + find(parent, c - 97))
    return bytes(out)


seed = 1061


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, k):
    return bytes(97 + next_random() % k for _ in range(n))


def main():
    s1s, s2s = [], []
    for p in range(100):
        k = 2 + p % 25
        s1s.append(random_word(1000, k))
        s2s.append(random_word(1000, k))
    bases = [random_word(20000, 26) for _ in range(100)]
    calls = total = check = 0
    for p in range(100):
        for b in range(100):
            answer = smallest_equivalent(s1s[p], s2s[p], bases[b])
            s = 0
            for c in answer:
                s += c
            total += s
            check = (check * 31 + s % 1000003) % 1000000007
            calls += 1
    print(f"{calls} calls: letters sum {total}, checksum {check}")


main()

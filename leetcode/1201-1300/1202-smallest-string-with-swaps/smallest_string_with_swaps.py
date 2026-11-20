# LeetCode #1202: Smallest String With Swaps -- the ★ arm in Python: the
# pairs join indices in a union-find (path halving, union by size), and
# each group's letters, sorted, go back to its indices in rising order.


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
        a, b = find(parent, p[0]), find(parent, p[1])
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
    groups = [[] for _ in range(n)]
    for i in range(n):
        groups[find(parent, i)].append(i)
    out = list(s)
    for g in groups:
        letters = sorted(s[i] for i in g)
        for k, i in enumerate(g):
            out[i] = letters[k]
    return "".join(out)


# ---- test harness ---------------------------------------------------------

seed = 1202


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    high = next_random()
    low = next_random()
    return high * 32768 + low


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def random_text(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def show(v):
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    return str(v)


cases = [
    ("dcab", [[0, 3], [1, 2]]),
    ("dcab", [[0, 3], [1, 2], [0, 2]]),
    ("cba", [[0, 1], [1, 2]]),
    ("zyx", []),
    ("q", [[0, 0]]),
    ("udyyek", [[3, 3], [3, 0], [5, 1], [3, 1], [3, 4], [3, 5]]),
    ("pwqlmqm", [[5, 3], [3, 0], [5, 1], [1, 1], [1, 5], [3, 0], [0, 2]]),
    ("abcd", [[3, 0], [0, 3]]),
]
for s, pairs in cases:
    print(f"{s} {show(pairs)}: {smallest_string_with_swaps(s, pairs)}")
changed = check = 0
for _ in range(1000):
    n = next_random() % 12 + 1
    s = random_text(n, 5)
    m = next_random() % 9
    pairs = []
    for _ in range(m):
        a = next_random() % n
        b = next_random() % n
        pairs.append([a, b])
    t = smallest_string_with_swaps(s, pairs)
    if t != s:
        changed += 1
    check = (check * 131 + digest(t)) % 1000000007
print(f"1000 random strings: {changed} changed, checksum {check}")
n = 100000
s = random_text(n, 26)
pairs = []
for _ in range(n):
    a = big() % n
    b = big() % n
    pairs.append([a, b])
t = smallest_string_with_swaps(s, pairs)
print(f"100000 letters, 100000 random pairs: digest {digest(t)}, starts {t[:12]}")
t = smallest_string_with_swaps(s, [[i, i + 2] for i in range(n - 2)])
print(f"100000 letters, each joined to the one two on: digest {digest(t)}, starts {t[:12]}")

# LeetCode #2157: Groups of Strings -- the benchmark's Python mirror of
# groups.kara.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def unite(parent, size, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return
    big, small = (ra, rb) if size[ra] >= size[rb] else (rb, ra)
    parent[small] = big
    size[big] += size[small]


def group_strings(words):
    n = len(words)
    masks = []
    for w in words:
        m = 0
        for b in w.encode():
            m |= 1 << (b - 97)
        masks.append(m)
    parent = list(range(n))
    size = [1] * n
    first = {}
    for i in range(n):
        j = first.get(masks[i])
        if j is not None:
            unite(parent, size, i, j)
        else:
            first[masks[i]] = i
    blanked = {}
    for i in range(n):
        for bit in range(26):
            if (masks[i] >> bit) & 1 == 1:
                less = masks[i] ^ (1 << bit)
                j = first.get(less)
                if j is not None:
                    unite(parent, size, i, j)
                j = blanked.get(less)
                if j is not None:
                    unite(parent, size, i, j)
                else:
                    blanked[less] = i
    groups = 0
    largest = 0
    for i in range(n):
        if find(parent, i) == i:
            groups += 1
            largest = max(largest, size[i])
    return [groups, largest]


seed = 2157


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word():
    length = next_random() % 8 + 1
    w = ""
    while len(w) < length:
        c = chr(97 + next_random() % 20)
        if c not in w:
            w += c
    return w


def main():
    lists = [[word() for _ in range(5000)] for _ in range(4)]
    total = 0
    check = 0
    for rnd in range(25):
        for l in range(4):
            at = next_random() % 5000
            lists[l][at] = word()
            answer = group_strings(lists[l])
            total += answer[0]
            check = (check * 31 + answer[0] * 10007 + answer[1] + rnd) % 1000000007
    print(f"100 solves: {total} groups in all, checksum {check}")


main()

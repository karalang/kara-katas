# LeetCode #2157: Groups of Strings -- the Python mirror of groups.kara,
# the ★ arm: a union-find over the words, joined through a map of each
# set's first word and a map of each set with one letter blanked out.


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
        for c in w:
            m |= 1 << (ord(c) - ord("a"))
        masks.append(m)
    parent = list(range(n))
    size = [1] * n
    first = {}
    for i in range(n):
        if masks[i] in first:
            unite(parent, size, i, first[masks[i]])
        else:
            first[masks[i]] = i
    blanked = {}
    for i in range(n):
        for bit in range(26):
            if (masks[i] >> bit) & 1 == 1:
                less = masks[i] ^ (1 << bit)
                if less in first:
                    unite(parent, size, i, first[less])
                if less in blanked:
                    unite(parent, size, i, blanked[less])
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


def word(most, alphabet):
    length = next_random() % most + 1
    w = ""
    while len(w) < length:
        c = chr(ord("a") + next_random() % alphabet)
        if c not in w:
            w += c
    return w


def show(words):
    print(f"[{', '.join(words)}] -> {group_strings(words)}")


def main():
    show(["a", "b", "ab", "cde"])
    show(["a", "ab", "abc"])
    show(["xyz"])
    show(["ab", "ba"])
    show(["ab", "cd", "ef"])
    show(["ab", "ac", "bc"])
    groups = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 8 + 1
        alphabet = [4, 6, 26][rnd % 3]
        words = [word(4, alphabet) for _ in range(n)]
        answer = group_strings(words)
        groups += answer[0]
        check = (check * 31 + answer[0] * 100 + answer[1] + n) % 1000000007
    print(f"2000 lists: {groups} groups in all, checksum {check}")
    for most, alphabet in [(5, 10), (26, 26)]:
        words = [word(most, alphabet) for _ in range(20000)]
        answer = group_strings(words)
        print(f"20000 words of 1 to {most} letters from {alphabet}: {answer[0]} groups, the largest {answer[1]}")


main()

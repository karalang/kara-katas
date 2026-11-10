# LeetCode #2092: Find All People With Secret -- Python mirror of the ★
# arm's benchmark (secret.kara): the same 10 gatherings, each answered 4
# times by the same stable sort and union-find over lists.

seed = 2092


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def find_all_people(n, meetings, first_person):
    srt = sorted(meetings, key=lambda m: m[2])
    parent = list(range(n))
    parent[first_person] = 0
    i = 0
    while i < len(srt):
        j = i
        while j < len(srt) and srt[j][2] == srt[i][2]:
            x, y, _ = srt[j]
            rx, ry = find(parent, x), find(parent, y)
            if rx < ry:
                parent[ry] = rx
            else:
                parent[rx] = ry
            j += 1
        for k in range(i, j):
            x, y, _ = srt[k]
            if find(parent, x) != 0:
                parent[x] = x
            if find(parent, y) != 0:
                parent[y] = y
        i = j
    return [p for p in range(n) if find(parent, p) == 0]


def main():
    n = 100000
    gatherings = []
    for _ in range(10):
        ms = []
        for _ in range(100000):
            x = (next_random() * 32768 + next_random()) % n
            y = (x + 1 + (next_random() * 32768 + next_random()) % (n - 1)) % n
            ms.append((x, y, next_random() % 1000 + 1))
        gatherings.append(ms)
    total = check = 0
    for rnd in range(4):
        for g in range(10):
            got = find_all_people(n, gatherings[g], rnd * 10 + g + 1)
            total += len(got)
            for p in got:
                check = (check * 31 + p) % 1000000007
    print(f"40 answers: {total} people, checksum {check}")


main()

# LeetCode #2092: Find All People With Secret -- Python mirror of the ★ arm
# (secret.kara): the meetings sorted by time, each time joined in a
# union-find rooted at person 0 and cut loose again where it is not joined
# to 0. Output is byte-identical.

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


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        (6, [(1, 2, 5), (2, 3, 8), (1, 5, 10)], 1),
        (4, [(3, 1, 3), (1, 2, 2), (0, 3, 3)], 3),
        (5, [(3, 4, 2), (1, 2, 1), (2, 3, 1)], 1),
        (2, [], 1),
        (3, [(1, 2, 0)], 1),
        (4, [(2, 3, 1), (1, 2, 2)], 1),
        (5, [(1, 4, 3), (0, 4, 3)], 2),
    ]
    for n, meetings, first in examples:
        print(f"{n} people, first {first}, {len(meetings)} meetings -> {show(find_all_people(n, meetings, first))}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 59 + 2
        m = next_random() % 81
        meetings = []
        for _ in range(m):
            x = next_random() % n
            y = (x + 1 + next_random() % (n - 1)) % n
            meetings.append((x, y, next_random() % 10 + 1))
        first = next_random() % (n - 1) + 1
        got = find_all_people(n, meetings, first)
        total += len(got)
        for p in got:
            check = (check * 31 + p + 1) % 1000000007
        check = (check * 31 + 1000) % 1000000007
    print(f"2000 gatherings: {total} people, checksum {check}")
    n = 100000
    meetings = []
    for _ in range(100000):
        x = (next_random() * 32768 + next_random()) % n
        y = (x + 1 + (next_random() * 32768 + next_random()) % (n - 1)) % n
        meetings.append((x, y, (next_random() * 32768 + next_random()) % 100000 + 1))
    got = find_all_people(n, meetings, 1)
    c = 0
    for p in got:
        c = (c * 31 + p + 1) % 1000000007
    print(f"100000 people: {len(got)} know, checksum {c}")
    rising = [(i, i + 1, i) for i in range(1, n - 1)]
    falling = [(i, i + 1, n - i) for i in range(1, n - 1)]
    print(f"rising chain: {len(find_all_people(n, rising, 1))} know; falling chain: {len(find_all_people(n, falling, 1))} know")


main()

# LeetCode #2201: Count Artifacts That Can Be Extracted -- Python mirror of
# dig.kara (the ★ arm): the dug cells in a set, each as r * n + c, and an
# artifact counted when every cell of its rectangle is in the set.


def dig_artifacts(n, artifacts, dig):
    dug = set()
    for d in dig:
        dug.add(d[0] * n + d[1])
    count = 0
    for a in artifacts:
        whole = True
        for r in range(a[0], a[2] + 1):
            for c in range(a[1], a[3] + 1):
                if r * n + c not in dug:
                    whole = False
        if whole:
            count += 1
    return count


# ---- test harness ---------------------------------------------------------

seed = 2201


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def random_site(n, tries, digs):
    shapes = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (1, 4), (4, 1)]
    taken = set()
    artifacts = []
    for _ in range(tries):
        h, w = shapes[next_random() % 8]
        if h > n or w > n:
            continue
        r = wide_random() % (n - h + 1)
        c = wide_random() % (n - w + 1)
        free = all((i * n + j) not in taken for i in range(r, r + h) for j in range(c, c + w))
        if free:
            for i in range(r, r + h):
                for j in range(c, c + w):
                    taken.add(i * n + j)
            artifacts.append([r, c, r + h - 1, c + w - 1])
    dug = set()
    dig = []
    while len(dig) < digs:
        cell = wide_random() % (n * n)
        if cell not in dug:
            dug.add(cell)
            dig.append([cell // n, cell % n])
    return artifacts, dig


def fmt(rows):
    return "[" + ", ".join("[" + ", ".join(map(str, r)) + "]" for r in rows) + "]"


def show(n, artifacts, dig):
    print(f"n {n}, {fmt(artifacts)}, dig {fmt(dig)} -> {dig_artifacts(n, artifacts, dig)}")


def main():
    show(2, [[0, 0, 0, 0], [0, 1, 1, 1]], [[0, 0], [0, 1]])
    show(2, [[0, 0, 0, 0], [0, 1, 1, 1]], [[0, 0], [0, 1], [1, 1]])
    show(3, [[0, 0, 1, 1]], [[2, 2]])
    show(1, [[0, 0, 0, 0]], [[0, 0]])
    show(3, [[1, 1, 2, 2]], [[1, 1], [1, 2], [2, 1]])
    show(4, [[3, 0, 3, 3], [0, 0, 1, 0]], [[3, 3], [3, 1], [3, 0], [3, 2], [1, 0]])
    found = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 12 + 1
        tries = next_random() % 20 + 1
        digs = next_random() % (n * n // 2 + 1) + 1
        artifacts, dig = random_site(n, tries, digs)
        if not artifacts:
            continue
        count = dig_artifacts(n, artifacts, dig)
        found += count
        check = (check * 31 + count + len(artifacts)) % 1000000007
    print(f"2000 sites: {found} extracted, checksum {check}")
    artifacts, dig = random_site(1000, 100000, 100000)
    print(f"n 1000: {len(artifacts)} artifacts, {len(dig)} dug, {dig_artifacts(1000, artifacts, dig)} extracted")


main()

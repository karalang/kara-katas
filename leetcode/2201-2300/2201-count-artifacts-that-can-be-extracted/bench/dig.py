# benchmark's Python mirror of dig.kara (LeetCode #2201, the ★ arm): the
# dug cells in a set, each as r * n + c.


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


seed = 2201


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def site(n, tries, digs):
    shapes = [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (1, 4), (4, 1)]
    taken = [False] * (n * n)
    artifacts = []
    for _ in range(tries):
        h, w = shapes[next_random() % 8]
        r = wide_random() % (n - h + 1)
        c = wide_random() % (n - w + 1)
        free = True
        for i in range(r, r + h):
            for j in range(c, c + w):
                if taken[i * n + j]:
                    free = False
        if free:
            for i in range(r, r + h):
                for j in range(c, c + w):
                    taken[i * n + j] = True
            artifacts.append((r, c, r + h - 1, c + w - 1))
    dug = [False] * (n * n)
    dig = []
    while len(dig) < digs:
        cell = wide_random() % (n * n)
        if not dug[cell]:
            dug[cell] = True
            dig.append((cell // n, cell % n))
    return artifacts, dig


def main():
    sites = [site(1000, 20000, 300000) for _ in range(8)]
    check = 0
    for _ in range(10):
        for artifacts, dig in sites:
            count = dig_artifacts(1000, artifacts, dig)
            check = (check * 31 + count + len(artifacts)) % 1000000007
    print(f"10 passes over 8 sites: checksum {check}")


main()

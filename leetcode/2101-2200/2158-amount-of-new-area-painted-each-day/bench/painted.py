# LeetCode #2158: Amount of New Area Painted Each Day -- the benchmark's
# Python mirror of painted.kara.


def first_unpainted(nxt, x):
    while nxt[x] != x:
        nxt[x] = nxt[nxt[x]]
        x = nxt[x]
    return x


def amount_painted(paint):
    wall = max(p[1] for p in paint)
    nxt = list(range(wall + 1))
    log = []
    for p in paint:
        painted = 0
        x = first_unpainted(nxt, p[0])
        while x < p[1]:
            painted += 1
            nxt[x] = x + 1
            x = first_unpainted(nxt, x + 1)
        log.append(painted)
    return log


seed = 2158


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def segment():
    length = wide_random() % 500 + 1
    start = wide_random() % (50000 - length + 1)
    return [start, start + length]


def main():
    lists = [[segment() for _ in range(100000)] for _ in range(4)]
    total = 0
    check = 0
    for rnd in range(5):
        for l in range(4):
            at = wide_random() % 100000
            lists[l][at] = segment()
            log = amount_painted(lists[l])
            for day, a in enumerate(log):
                total += a
                check = (check * 31 + a * (day + 1) + rnd) % 1000000007
    print(f"20 solves: {total} units in all, checksum {check}")


main()

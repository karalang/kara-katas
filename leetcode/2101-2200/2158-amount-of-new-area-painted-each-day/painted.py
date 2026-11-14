# LeetCode #2158: Amount of New Area Painted Each Day -- the Python mirror
# of painted.kara, the ★ arm: each unit points at the first unpainted unit
# at or after it, and the walks halve their paths.


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


def segment(width, most):
    length = wide_random() % min(most, width) + 1
    start = wide_random() % (width - length + 1)
    return [start, start + length]


def fmt(v):
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    return str(v)


def show(paint):
    print(f"{fmt(paint)} -> {fmt(amount_painted(paint))}")


def main():
    show([[1, 4], [4, 7], [5, 8]])
    show([[1, 4], [5, 8], [4, 7]])
    show([[1, 5], [2, 4]])
    show([[0, 1]])
    show([[3, 9], [3, 9]])
    show([[2, 3], [1, 4], [0, 5]])
    show([[0, 2], [4, 6], [2, 4]])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 8 + 1
        width = [10, 30, 100][rnd % 3]
        paint = [segment(width, width) for _ in range(n)]
        for a in amount_painted(paint):
            total += a
            check = (check * 31 + a + 1) % 1000000007
    print(f"2000 lists: {total} units in all, checksum {check}")
    for name, most in [("short", 50), ("any", 50000), ("whole", 0)]:
        paint = [[0, 50000] if most == 0 else segment(50000, most) for _ in range(100000)]
        log = amount_painted(paint)
        s = 0
        days = 0
        h = 0
        for a in log:
            s += a
            if a > 0:
                days += 1
            h = (h * 31 + a + 1) % 1000000007
        print(f"100000 days, {name}: {s} units on {days} days, checksum {h}")


main()

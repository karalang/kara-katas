# Benchmark for #587: Python mirror of the ★ arm (the monotone chain);
# see outer_trees.kara. Each call sorts a fresh list of the trees, builds
# the fence in another, sorts that and removes repeats.


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def outer_trees(trees):
    points = sorted(trees)
    fence = []
    for p in points:
        while len(fence) >= 2 and cross(fence[-2], fence[-1], p) < 0:
            fence.pop()
        fence.append(p)
    lower = len(fence)
    for p in reversed(points):
        while len(fence) > lower and cross(fence[-2], fence[-1], p) < 0:
            fence.pop()
        fence.append(p)
    fence.sort()
    return [p for i, p in enumerate(fence) if i == 0 or p != fence[i - 1]]


# ---- benchmark --------------------------------------------------------------

seed = 587


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 50
    rounds = 300
    gardens = []
    for _ in range(count):
        size = 1000 + next_random() % 2001
        taken = [False] * (101 * 101)
        trees = []
        while len(trees) < size:
            x = next_random() % 101
            y = next_random() % 101
            if not taken[x * 101 + y]:
                taken[x * 101 + y] = True
                trees.append((x, y))
        gardens.append(trees)
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            fence = outer_trees(gardens[p])
            total += len(fence)
            checksum = (checksum * 31 + sum(t[0] * 101 + t[1] for t in fence)) % 1000000007
    print(f"{count} gardens, {rounds} rounds: {total} on the fence, checksum {checksum}")


main()

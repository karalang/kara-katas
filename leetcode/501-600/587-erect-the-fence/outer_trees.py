# LeetCode #587: Erect the Fence -- Python mirror of the ★ arm (the
# monotone chain); see outer_trees.kara.


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


# ---- test harness -----------------------------------------------------------

seed = 587


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def forest(count, size):
    taken = [False] * (size * size)
    trees = []
    while len(trees) < count:
        x = step() % size
        y = step() % size
        if not taken[x * size + y]:
            taken[x * size + y] = True
            trees.append((x, y))
    return trees


def sorted_fence(trees):
    return sorted(outer_trees(trees))


def checksum_of(fence):
    checksum = 0
    for t in fence:
        checksum = (checksum * 31 + t[0] * 101 + t[1]) % 1000000007
    return checksum


def show(name, trees):
    print(f"{name}: {sorted_fence(trees)}")


def summary(name, trees):
    fence = sorted_fence(trees)
    print(f"{name}: {len(fence)} on the fence, checksum {checksum_of(fence)}")


def main():
    show("example 1", [(1, 1), (2, 2), (2, 0), (2, 4), (3, 3), (4, 2)])
    show("example 2", [(1, 2), (2, 2), (4, 2)])
    show("one tree", [(5, 5)])
    show("two trees", [(0, 0), (3, 4)])
    show("upright line", [(2, 0), (2, 4), (2, 1), (2, 3), (2, 2)])
    show("slanting line", [(0, 0), (3, 3), (1, 1), (2, 2)])
    show("3 by 3 square", [(x, y) for x in range(3) for y in range(3)])
    show("triangle", [(0, 0), (4, 0), (0, 4), (2, 0), (2, 2), (0, 2), (1, 1)])
    show("one inside", [(0, 0), (10, 0), (0, 10), (3, 3)])
    total = 0
    checksum = 0
    for _ in range(300):
        count = 1 + step() % 30
        fence = sorted_fence(forest(count, 11))
        total += len(fence)
        checksum = (checksum * 31 + checksum_of(fence)) % 1000000007
    print(f"300 random gardens: {total} on the fence, checksum {checksum}")
    summary("3000 at random", forest(3000, 101))
    summary("50 by 60 grid", [(x, y) for x in range(50) for y in range(60)])
    diamond = [(x, y) for x in range(101) for y in range(101) if abs(x - 50) + abs(y - 50) <= 38]
    summary("diamond", diamond)


main()

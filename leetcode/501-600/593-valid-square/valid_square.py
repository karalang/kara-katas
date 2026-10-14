# LeetCode #593: Valid Square -- the six distances, sorted.
#
# Mirrors valid_square.kara: four points make a square exactly when, of
# the six squared distances between them, the four smallest are equal
# and not 0 and the two largest are equal and twice a side.


def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def valid_square(p1, p2, p3, p4):
    d = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), dist(p2, p3), dist(p2, p4), dist(p3, p4)])
    return d[0] > 0 and d[0] == d[3] and d[4] == d[5] and d[4] == 2 * d[0]


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(p1, p2, p3, p4):
    ok = "true" if valid_square(p1, p2, p3, p4) else "false"
    print(f"[{p1[0]},{p1[1]}] [{p2[0]},{p2[1]}] [{p3[0]},{p3[1]}] [{p4[0]},{p4[1]}] -> {ok}")


def random_points(seed):
    kind = step(seed) % 3
    if kind == 2:
        points = []
        for _ in range(4):
            x = step(seed) % 7 - 3
            y = step(seed) % 7 - 3
            points.append([x, y])
        return points
    x = step(seed) % 2001 - 1000
    y = step(seed) % 2001 - 1000
    dx = step(seed) % 41 - 20
    dy = step(seed) % 41 - 20
    if dx == 0 and dy == 0:
        dx = 1
    points = [[x, y], [x + dx, y + dy], [x + dx - dy, y + dy + dx], [x - dy, y + dx]]
    if kind == 1:
        k = step(seed) % 4
        c = step(seed) % 2
        points[k][c] += 1 if step(seed) % 2 == 0 else -1
    for k in range(3):
        j = k + step(seed) % (4 - k)
        points[k], points[j] = points[j], points[k]
    return points


def main():
    show([0, 0], [1, 1], [1, 0], [0, 1])
    show([0, 0], [1, 1], [1, 0], [0, 12])
    show([1, 0], [-1, 0], [0, 1], [0, -1])
    show([0, 0], [2, 1], [1, 3], [-1, 2])
    show([-10000, -10000], [10000, 10000], [-10000, 10000], [10000, -10000])
    show([0, 0], [2, 0], [2, 1], [0, 1])
    show([0, 0], [2, 1], [3, 3], [1, 2])
    show([0, 0], [1, 0], [0, 1], [2, 2])
    show([5, 5], [5, 5], [5, 5], [5, 5])
    show([0, 0], [0, 0], [1, 1], [1, 1])
    show([0, 0], [1, 0], [0, 1], [0, 1])
    show([0, 0], [1, 0], [2, 0], [1, 1])
    seed = [593]
    squares = 0
    checksum = 0
    for t in range(1000):
        p = random_points(seed)
        if valid_square(p[0], p[1], p[2], p[3]):
            squares += 1
            checksum = (checksum * 31 + t + 1) % 1000000007
    print(f"1000 random cases: {squares} squares, checksum {checksum}")


main()

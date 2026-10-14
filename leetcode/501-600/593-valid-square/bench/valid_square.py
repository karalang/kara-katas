# Benchmark for #593: Python mirror of the ★ arm (the six distances,
# sorted); see valid_square.kara.


def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def valid_square(p1, p2, p3, p4):
    d = sorted([dist(p1, p2), dist(p1, p3), dist(p1, p4), dist(p2, p3), dist(p2, p4), dist(p3, p4)])
    return d[0] > 0 and d[0] == d[3] and d[4] == d[5] and d[4] == 2 * d[0]


# ---- benchmark ---------------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


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
    count = 1000
    rounds = 20000
    seed = [593]
    cases = [random_points(seed) for _ in range(count)]
    squares = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = cases[(rnd * 7 + g) % count]
            if valid_square(p[0], p[1], p[2], p[3]):
                squares += 1
                checksum = (checksum * 31 + g + 1) % 1000000007
    print(f"{count} cases, {rounds} rounds: {squares} squares, checksum {checksum}")


main()

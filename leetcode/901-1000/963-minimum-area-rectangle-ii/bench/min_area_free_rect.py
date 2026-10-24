# Benchmark: LeetCode #963 Minimum Area Rectangle II -- the ★ arm,
# diagonals grouped by centre, on 50 points packed into small grids.
# Mirrors min_area_free_rect.kara.


def min_area_free_rect(points):
    n = len(points)
    groups = {}
    for i in range(n):
        for j in range(i + 1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            key = (points[i][0] + points[j][0], points[i][1] + points[j][1], dx * dx + dy * dy)
            groups.setdefault(key, []).append((i, j))
    best = 0
    for pairs in groups.values():
        for x in range(len(pairs)):
            for y in range(x + 1, len(pairs)):
                i = pairs[x][0]
                k, l = pairs[y]
                ux = points[k][0] - points[i][0]
                uy = points[k][1] - points[i][1]
                vx = points[l][0] - points[i][0]
                vy = points[l][1] - points[i][1]
                area = abs(ux * vy - uy * vx)
                if best == 0 or area < best:
                    best = area
    return float(best)


seed = 963


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def has(points, x, y):
    return any(p[0] == x and p[1] == y for p in points)


def packed(n, top):
    out = []
    while len(out) < n:
        x = next_random() % (top + 1)
        y = next_random() % (top + 1)
        if not has(out, x, y):
            out.append([x, y])
    return out


def main():
    rounds = 40
    cases = [packed(50, 7 + i % 10) for i in range(50)]
    total = 0.0
    check = 0
    for r in range(rounds):
        for i in range(50):
            c = (r + i) % 50
            top = 7 + c % 10
            p = next_random() % 50
            x = next_random() % (top + 1)
            y = next_random() % (top + 1)
            if not has(cases[c], x, y):
                cases[c][p] = [x, y]
            a = min_area_free_rect(cases[c])
            total += a
            check = (check * 31 + int(a) + i) % 1000000007
    print(f"{rounds} rounds over 50 cases of 50 points: the areas sum to {total:.5f}, checksum {check}")


main()

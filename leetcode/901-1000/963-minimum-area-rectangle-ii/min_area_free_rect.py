# LeetCode #963: Minimum Area Rectangle II -- diagonals by centre.
#
# Mirrors min_area_free_rect.kara: pairs of points grouped by the sum of
# their ends and their squared length; any two pairs in a group are the
# diagonals of a rectangle, its area the cross product of two sides.


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n, top):
    seen = set()
    out = []
    while len(out) < n:
        x = next_random() % (top + 1)
        y = next_random() % (top + 1)
        if x * 1000000 + y not in seen:
            seen.add(x * 1000000 + y)
            out.append([x, y])
    return out


def show(points):
    return "[" + ",".join(f"[{p[0]},{p[1]}]" for p in points) + "]"


def main():
    global seed
    cases = [
        [[1, 2], [2, 1], [1, 0], [0, 1]],
        [[0, 1], [2, 1], [1, 1], [1, 0], [2, 0]],
        [[0, 3], [1, 2], [3, 1], [1, 3], [2, 1]],
        [[3, 1], [1, 1], [0, 1], [2, 1], [3, 3], [3, 2], [0, 2], [2, 3]],
        [[0, 0]],
        [[0, 0], [0, 1], [1, 0], [1, 1]],
        [[0, 2], [2, 0], [4, 2], [2, 4]],
        [[1, 0], [4, 1], [3, 4], [0, 3]],
        [[0, 0], [0, 40000], [40000, 0], [40000, 40000]],
        [[0, 0], [1, 1], [2, 2], [3, 3]],
        [[0, 0], [2, 0], [2, 1], [0, 1], [1, 0], [1, 1]],
    ]
    for points in cases:
        print(f"{show(points)}: {min_area_free_rect(points):.5f}")
    seed = 963
    count = 0
    total = 0.0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 10
        points = random_points(n, 4)
        a = min_area_free_rect(points)
        count += n
        total += a
        check = (check * 31 + int(a)) % 1000000007
    print(f"300 random cases of {count} points: the areas sum to {total:.5f}, checksum {check}")
    big = random_points(50, 40000)
    print(f"50 random points: {min_area_free_rect(big):.5f}")
    grid = [[4000 * (i % 10), 4000 * (i // 10)] for i in range(50)]
    print(f"a 10 by 5 grid 4000 apart: {min_area_free_rect(grid):.5f}")
    circle = []
    x = -1105
    while len(circle) < 50:
        y = 0
        while y * y + x * x < 1105 * 1105:
            y += 1
        if y * y + x * x == 1105 * 1105 and y > 0:
            circle.append([20000 + x, 20000 + y])
            circle.append([20000 - x, 20000 - y])
        x += 1
    print(f"50 points on one circle: {min_area_free_rect(circle):.5f}")
    tilted = [[20000 + 3 * (i % 7) - 4 * (i // 7), 100 + 4 * (i % 7) + 3 * (i // 7)] for i in range(49)]
    tilted.append([0, 0])
    print(f"a 7 by 7 grid tilted, and a stray point: {min_area_free_rect(tilted):.5f}")


main()

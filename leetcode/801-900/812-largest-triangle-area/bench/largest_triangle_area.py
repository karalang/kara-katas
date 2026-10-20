# LeetCode 812 -- Largest Triangle Area: the bench, with the ★ arm's
# every triple of points.

seed = 812


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def largest_triangle_area(points):
    n = len(points)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                twice = twice_area(points[i], points[j], points[k])
                if twice > best:
                    best = twice
    return best / 2.0


def twice_area(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


# A point with coordinates from -50 to 50 that is not in `points`.
def new_point(points):
    while True:
        p = (next_random() % 101 - 50, next_random() % 101 - 50)
        if p not in points:
            return p


# 64 sets of 50 distinct points are made once. Each round moves one point
# of the next set to a new place and finds that set's largest triangle.
def main():
    sets = []
    for _ in range(64):
        points = []
        for _ in range(50):
            points.append(new_point(points))
        sets.append(points)
    rounds = 60000
    total = 0.0
    check = 0
    for r in range(rounds):
        k = r % 64
        p = new_point(sets[k])
        sets[k][r // 64 % 50] = p
        area = largest_triangle_area(sets[k])
        total += area
        check = (check * 131 + int(area * 2.0)) % 1000000007
    print(f"{rounds} rounds of 50 points: total area {total}, checksum {check}")


main()

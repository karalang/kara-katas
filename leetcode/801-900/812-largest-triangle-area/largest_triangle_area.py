# LeetCode 812 — Largest Triangle Area, every triple of points (mirror of the ★ arm).


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(points):
    print(f"points = {points} -> {largest_triangle_area(points)}")


def random_points(n, r):
    side = 2 * r + 1
    taken = [False] * (side * side)
    points = []
    while len(points) < n:
        x = next_random() % side
        y = next_random() % side
        if not taken[x * side + y]:
            taken[x * side + y] = True
            points.append((x - r, y - r))
    return points


def main():
    global seed
    show([(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)])
    show([(1, 0), (0, 0), (0, 1)])
    show([(0, 0), (1, 1), (2, 2)])
    show([(-50, -50), (50, -50), (50, 50), (-50, 50)])
    show([(0, 0), (3, 1), (1, 3), (2, 2), (1, 1)])
    show([(-50, 0), (50, 1), (0, -50), (1, 49), (0, 0)])
    seed = 812
    show(random_points(50, 50))
    line = [(2 * i - 49, 49 - 2 * i) for i in range(50)]
    print(f"50 points on a line -> {largest_triangle_area(line)}")
    total = 0.0
    check = 0
    for r in range(300):
        n = 3 + next_random() % 20
        area = largest_triangle_area(random_points(n, 2 + r % 9))
        total += area
        check = (check * 131 + int(area * 2.0) + r) % 1000000007
    print(f"300 random rounds of 3 to 22 points: total area {total}, checksum {check}")


main()

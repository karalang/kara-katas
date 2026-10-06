# LeetCode #356: Line Reflection -- Python mirror of line_reflection.kara.
# The only candidate line is 2c = min x + max x; the set reflects exactly when
# every point's image (min + max - x, y) is a point of the set.


def is_reflected(points):
    if not points:
        return True
    lo = min(x for x, _ in points)
    hi = max(x for x, _ in points)
    seen = set(points)
    total = lo + hi
    return all((total - x, y) in seen for x, y in points)


def show(label, points):
    print(f"{label}: {'true' if is_reflected(points) else 'false'}")


def main():
    show("example 1", [(1, 1), (-1, 1)])
    show("example 2", [(1, 1), (-1, -1)])

    show("no points", [])
    show("one point", [(5, -3)])
    show("a point on the line with its pair", [(0, 0), (-2, 4), (2, 4)])
    show("duplicates on one side", [(1, 1), (1, 1), (3, 1)])
    show("half-integer line", [(0, 7), (1, 7), (0, 2), (1, 2)])
    show("same xs, wrong ys", [(0, 0), (4, 1)])
    show("column of points on the line", [(3, 0), (3, 5), (3, -5)])
    show("one stray point", [(-5, 0), (5, 0), (-1, 2), (1, 2), (2, 9)])
    show("negative coordinates", [(-10, -1), (-6, -1), (-8, 3)])
    show("large coordinates", [(-100000000, 0), (100000000, 0), (0, 100000000)])

    seed = 356
    yes = 0
    checksum = 0
    for case in range(2000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = (seed // 65536) % 12
        seed = (seed * 1103515245 + 12345) % 2147483648
        center = (seed // 65536) % 21 - 10
        points = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            x = (seed // 65536) % 9 - 4
            seed = (seed * 1103515245 + 12345) % 2147483648
            y = (seed // 65536) % 5
            points.append((x, y))
            if case % 2 == 0:
                points.append((center - x, y))
        seed = (seed * 1103515245 + 12345) % 2147483648
        if case % 4 == 0 and points:
            i = (seed // 65536) % len(points)
            points[i] = (points[i][0] + 1, points[i][1])
        r = is_reflected(points)
        if r:
            yes += 1
        checksum = (checksum * 3 + (1 if r else 2)) % 1000000007
    print(f"2000 random sets: {yes} reflect, checksum {checksum}")


if __name__ == "__main__":
    main()

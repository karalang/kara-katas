# LeetCode #1266: Minimum Time Visiting All Points -- Python mirror of the
# ★ arm (the larger of the two gaps between neighbouring points, summed),
# with the same harness.


def min_time_to_visit_all_points(points):
    return sum(max(abs(b[0] - a[0]), abs(b[1] - a[1])) for a, b in zip(points, points[1:]))


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_points(n, top, rng):
    out = []
    for _ in range(n):
        x = rng.next() % (2 * top + 1) - top
        y = rng.next() % (2 * top + 1) - top
        out.append([x, y])
    return out


def main():
    print(f"{min_time_to_visit_all_points([[1, 1], [3, 4], [-1, 0]])} {min_time_to_visit_all_points([[3, 2], [-2, 2]])}")
    rng = Rng(1266)
    total = check = 0
    for case in range(2000):
        n = rng.next() % 100 + 1
        top = 5 if case % 2 == 0 else 1000
        t = min_time_to_visit_all_points(random_points(n, top, rng))
        total += t
        check = (check * 131 + t) % 1000000007
    print(f"2000 random walks: {total} seconds, checksum {check}")
    corners = [[-1000, -1000] if i % 2 == 0 else [1000, 1000] for i in range(100)]
    line = [[i * 20 - 1000, 7] for i in range(100)]
    print(f"{min_time_to_visit_all_points(corners)} {min_time_to_visit_all_points(line)}")


main()

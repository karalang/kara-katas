# LeetCode #1266 bench, in Python: the ★ arm (the larger of the two gaps
# between neighbouring points, summed over each pair of neighbours) on 1000
# random walks of 100 points from -1000 to 1000 built once, 3000 rounds;
# every answer folded into a checksum.


def min_time_to_visit_all_points(points):
    return sum(max(abs(b[0] - a[0]), abs(b[1] - a[1])) for a, b in zip(points, points[1:]))


def main():
    seed = 1266

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    walks = []
    for _ in range(1000):
        walk = []
        for _ in range(100):
            x = nr() % 2001 - 1000
            y = nr() % 2001 - 1000
            walk.append([x, y])
        walks.append(walk)
    check = 0
    for rnd in range(3000):
        for w in walks:
            check = (check * 131 + min_time_to_visit_all_points(w) + rnd) % 1000000007
    print(f"3000 rounds of 1000 walks of 100 points: checksum {check}")


main()

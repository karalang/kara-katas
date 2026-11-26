# LeetCode #1401 bench, Python: the same clamp and squared distance,
# workload and checksum as check_overlap.kara.


def check_overlap(radius, x_center, y_center, x1, y1, x2, y2):
    dx = min(max(x_center, x1), x2) - x_center
    dy = min(max(y_center, y1), y2) - y_center
    return dx * dx + dy * dy <= radius * radius


def main():
    seed = 1401
    cases = []
    for _ in range(100000):
        v = []
        for _ in range(5):
            seed = (seed * 1103515245 + 12345) % 2147483648
            v.append(seed % 2001 - 1000)
        seed = (seed * 1103515245 + 12345) % 2147483648
        w = 1 + seed % 300
        seed = (seed * 1103515245 + 12345) % 2147483648
        h = 1 + seed % 300
        v[0] = abs(v[0]) // 10 + 1
        v.append(v[3] + w)
        v.append(v[4] + h)
        cases.append(v)
    check = 0
    for rnd in range(1000):
        overlaps = 0
        for c in cases:
            if check_overlap(c[0] + rnd, c[1], c[2], c[3], c[4], c[5], c[6]):
                overlaps += 1
        check = (check * 131 + overlaps) % 1000000007
    print(f"1000 rounds over 10^5 circles and rectangles: checksum {check}")


main()

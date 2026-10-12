# LeetCode #452: Minimum Number of Arrows to Burst Balloons -- mirror of
# min_arrows.kara (greedy by end), with the same harness.


def find_min_arrow_shots(points):
    by_end = sorted(points, key=lambda p: p[1])
    arrows = 0
    arrow = 0
    for start, end in by_end:
        if arrows == 0 or start > arrow:
            arrows += 1
            arrow = end
    return arrows


# ---- test harness ---------------------------------------------------------


def listed(points):
    return ",".join(f"[{a},{b}]" for a, b in points)


def show(points):
    print(f"[{listed(points)}]: arrows {find_min_arrow_shots(points)}")


seed = 452


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([(10, 16), (2, 8), (1, 6), (7, 12)])
    show([(1, 2), (3, 4), (5, 6), (7, 8)])
    show([(1, 2), (2, 3), (3, 4), (4, 5)])
    show([(5, 5)])
    show([(1, 10), (2, 9), (3, 8), (4, 7)])
    show([(-2147483648, 2147483647)])
    show([(-2147483648, -2147483648), (2147483647, 2147483647)])
    show([(1, 3), (2, 4), (5, 7), (6, 8), (3, 5)])
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = 1 + next_random() % 200
        span = [10, 100, 10000, 4294967296][next_random() % 4]
        width = [1, 6, 51, 2147483648][next_random() % 4]
        points = []
        for _ in range(n):
            r = next_random() * 65536
            r = (r + next_random()) * 2
            r += next_random() % 2
            start = r % span - span // 2
            w = next_random() * 65536
            w = (w + next_random()) % width
            end = min(start + w, 2147483647)
            points.append((start, end))
        arrows = find_min_arrow_shots(points)
        total += arrows
        checksum = (checksum * 31 + arrows) % 1000000007
    print(f"{count} random sets: {total} arrows, checksum {checksum}")


main()

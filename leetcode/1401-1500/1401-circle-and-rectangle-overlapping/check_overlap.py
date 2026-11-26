# LeetCode #1401: Circle and Rectangle Overlapping -- Python mirror of
# the ★ arm and its harness.


def check_overlap(radius, x_center, y_center, x1, y1, x2, y2):
    dx = min(max(x_center, x1), x2) - x_center
    dy = min(max(y_center, y1), y2) - y_center
    return dx * dx + dy * dy <= radius * radius


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def between(lo, hi):
    return lo + (next_random() * 32768 + next_random()) % (hi - lo + 1)


def text(b):
    return "true" if b else "false"


def main():
    global seed
    shown = [
        check_overlap(1, 0, 0, 1, -1, 3, 1),
        check_overlap(1, 1, 1, 1, -3, 2, -1),
        check_overlap(1, 0, 0, -1, 0, 0, 1),
        check_overlap(1, 1, 1, -3, -3, 3, 3),
        check_overlap(2, 0, 0, 1, 1, 3, 3),
        check_overlap(1, 0, 0, 1, 1, 3, 3),
    ]
    print(" ".join(text(b) for b in shown))
    counts = []
    for radius in range(1, 7):
        count = 0
        for x in range(-10, 11):
            for y in range(-10, 11):
                if check_overlap(radius, x, y, -3, -1, 2, 4):
                    count += 1
        counts.append(str(count))
    print(f"grid of 441 centers: {' '.join(counts)}")
    seed = 1401
    check = 0
    cases = 0
    overlaps = 0
    for i in range(20000):
        near = 50 if i % 2 == 0 else 2000
        radius = between(1, 20 if i % 2 == 0 else 2000)
        x = between(-10000 + near, 10000 - near)
        y = between(-10000 + near, 10000 - near)
        a = between(x - near, x + near)
        b = between(x - near, x + near)
        c = between(y - near, y + near)
        d = between(y - near, y + near)
        if a == b or c == d:
            continue
        cases += 1
        hit = check_overlap(radius, x, y, min(a, b), min(c, d), max(a, b), max(c, d))
        if hit:
            overlaps += 1
        check = (check * 131 + (2 if hit else 1)) % 1000000007
    print(f"{cases} random cases: {overlaps} overlap, checksum {check}")


main()

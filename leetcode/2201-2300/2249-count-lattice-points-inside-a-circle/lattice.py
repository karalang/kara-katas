# LeetCode #2249: Count Lattice Points Inside a Circle -- the Python
# mirror of lattice.kara: every lattice point of the box bounding all the
# circles tried against the circles until one holds it. O(box * circles).


def count_lattice_points(circles):
    left = min(x - r for x, _, r in circles)
    right = max(x + r for x, _, r in circles)
    bottom = min(y - r for _, y, r in circles)
    top = max(y + r for _, y, r in circles)
    count = 0
    for px in range(left, right + 1):
        for py in range(bottom, top + 1):
            for x, y, r in circles:
                dx = px - x
                dy = py - y
                if dx * dx + dy * dy <= r * r:
                    count += 1
                    break
    return count


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_circles(count, top):
    out = []
    for _ in range(count):
        x = next_random() % top + 1
        y = next_random() % top + 1
        r = next_random() % min(x, y) + 1
        out.append([x, y, r])
    return out


def main():
    global seed
    examples = [
        [[2, 2, 1]],
        [[2, 2, 2], [3, 4, 1]],
        [[1, 1, 1]],
        [[5, 5, 3], [5, 5, 3]],
        [[10, 10, 5], [10, 10, 2]],
        [[1, 1, 1], [100, 100, 100]],
    ]
    for circles in examples:
        print(f"{circles} -> {count_lattice_points(circles)}")
    seed = 2249
    total = 0
    check = 0
    for _ in range(2000):
        count = next_random() % 6 + 1
        circles = random_circles(count, 12)
        points = count_lattice_points(circles)
        total += points
        check = (check * 31 + points) % 1000000007
    print(f"2000 cases: {total} points, checksum {check}")
    circles = random_circles(200, 100)
    print(f"200 circles: {count_lattice_points(circles)}")
    circles = [[100, 100, 100] for _ in range(200)]
    print(f"200 of the largest: {count_lattice_points(circles)}")


main()

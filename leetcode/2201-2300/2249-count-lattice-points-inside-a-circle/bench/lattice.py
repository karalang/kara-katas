# LeetCode #2249: Count Lattice Points Inside a Circle -- the benchmark's
# Python mirror of lattice.kara: every point of the box bounding the
# circles tried against them until one holds it.


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


seed = 2249


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(100):
        circles = []
        for _ in range(200):
            x = next_random() % 100 + 1
            y = next_random() % 100 + 1
            r = next_random() % min(x, y) + 1
            circles.append((x, y, r))
        check = (check * 31 + count_lattice_points(circles)) % 1000000007
    print(f"100 cases of 200 circles: checksum {check}")


main()

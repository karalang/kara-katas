# LeetCode #1274: Number of Ships in a Rectangle -- Python mirror of the ★
# arm (divide and conquer by quarters, a rectangle with no ship counting
# none and a point with one counting one), with the same harness.


class Ocean:
    def __init__(self, ships):
        self.ships = ships
        self.calls = 0

    def has_ships(self, top_right, bottom_left):
        self.calls += 1
        return any(bottom_left[0] <= x <= top_right[0] and bottom_left[1] <= y <= top_right[1] for x, y in self.ships)


def count_ships(sea, top_right, bottom_left):
    if bottom_left[0] > top_right[0] or bottom_left[1] > top_right[1]:
        return 0
    if not sea.has_ships(top_right, bottom_left):
        return 0
    if top_right == bottom_left:
        return 1
    mx = (top_right[0] + bottom_left[0]) // 2
    my = (top_right[1] + bottom_left[1]) // 2
    return (
        count_ships(sea, [mx, my], bottom_left)
        + count_ships(sea, [top_right[0], my], [mx + 1, bottom_left[1]])
        + count_ships(sea, [mx, top_right[1]], [bottom_left[0], my + 1])
        + count_ships(sea, top_right, [mx + 1, my + 1])
    )


seed = 1274


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_ships(top_right, bottom_left, inside, outside):
    ships = []
    w = top_right[0] - bottom_left[0] + 1
    h = top_right[1] - bottom_left[1] + 1
    for _ in range(inside):
        a = next_random()
        p = (bottom_left[0] + a % w, bottom_left[1] + next_random() % h)
        if p not in ships:
            ships.append(p)
    for _ in range(outside):
        a = next_random()
        p = (a % 1001, next_random() % 1001)
        inside_it = bottom_left[0] <= p[0] <= top_right[0] and bottom_left[1] <= p[1] <= top_right[1]
        if not inside_it and p not in ships:
            ships.append(p)
    return ships


def run(ships, top_right, bottom_left):
    sea = Ocean(ships)
    n = count_ships(sea, top_right, bottom_left)
    return f"({n}, {'true' if sea.calls <= 400 else 'false'})", n, sea.calls <= 400


print(f"{run([(1, 1), (2, 2), (3, 3), (5, 5)], [4, 4], [0, 0])[0]} {run([(1, 1), (2, 2), (3, 3)], [1000, 1000], [0, 0])[0]}")
found = 0
within = 0
check = 0
for _ in range(1000):
    x0 = next_random() % 1001
    y0 = next_random() % 1001
    x1 = x0 + next_random() % (1001 - x0)
    y1 = y0 + next_random() % (1001 - y0)
    inside = next_random() % 11
    ships = random_ships([x1, y1], [x0, y0], inside, 10)
    _, n, ok = run(ships, [x1, y1], [x0, y0])
    found += n
    within += ok
    check = (check * 131 + n) % 1000000007
print(f"1000 random rectangles: {found} ships, {within} within 400 questions, checksum {check}")
spread = [(i * 111, 1000 - i * 97) for i in range(10)]
corner = [(1000 - i % 4, 1000 - i // 4) for i in range(10)]
line = [(i * 100 + 37, 500) for i in range(10)]
print(f"{run(spread, [1000, 1000], [0, 0])[0]} {run(corner, [1000, 1000], [0, 0])[0]} {run(line, [1000, 1000], [0, 0])[0]}")

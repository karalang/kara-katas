# LeetCode #1274 bench, in Python: the ★ arm (divide and conquer by
# quarters through the sea's interface) on 500 random seas of 10 ships in
# the whole 1001-by-1001 square and 10 more in a corner, drawn once, 30
# rounds; every count, and the number of questions asked, folded into a
# checksum.


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


seas = []
for _ in range(500):
    ships = []
    for i in range(20):
        span = 1001 if i < 10 else 30
        x = next_random() % span
        p = (x, next_random() % span)
        if p not in ships:
            ships.append(p)
    seas.append(ships)
check = 0
for rnd in range(30):
    for ships in seas:
        sea = Ocean(list(ships))
        n = count_ships(sea, [1000, 1000], [0, 0])
        check = (check * 131 + n + rnd) % 1000000007
        check = (check * 131 + sea.calls) % 1000000007
print(f"30 rounds of 500 seas: checksum {check}")

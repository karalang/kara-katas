# LeetCode #447: Number of Boomerangs -- mirror of
# number_of_boomerangs.kara (a map of distances per point).


def number_of_boomerangs(points):
    total = 0
    for i in range(len(points)):
        counts = {}
        for j in range(len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d = dx * dx + dy * dy
            counts[d] = counts.get(d, 0) + 1
        for c in counts.values():
            total += c * (c - 1)
    return total


def show(points):
    text = ",".join(f"[{x},{y}]" for x, y in points)
    print(f"[{text}]: {number_of_boomerangs(points)}")


seed = 447


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n, spread):
    seen = set()
    points = []
    while len(points) < n:
        x = next_random() % spread - spread // 2
        y = next_random() % spread - spread // 2
        if (x, y) not in seen:
            seen.add((x, y))
            points.append((x, y))
    return points


show([(0, 0), (1, 0), (2, 0)])
show([(1, 1), (2, 2), (3, 3)])
show([(1, 1)])
show([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])
show([(0, 0), (3, 4), (-4, 3), (5, 0), (0, -5)])
show([(-10000, -10000), (10000, 10000), (10000, -10000), (-10000, 10000)])
count = 300
total = 0
checksum = 0
for _ in range(count):
    n = 1 + next_random() % 80
    spread = [10, 20, 1000, 20001][next_random() % 4]
    if spread == 10:
        n = min(n, 60)
    answer = number_of_boomerangs(random_points(n, spread))
    total += answer
    checksum = (checksum * 31 + answer) % 1000000007
print(f"{count} random point sets: {total} boomerangs, checksum {checksum}")

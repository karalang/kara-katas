# LeetCode #1610: Maximum Number of Visible Points -- the Python mirror of
# visible.kara: each direction in degrees, sorted and doubled with 360
# more, and a window slid along it. `to_degrees` is written out as Rust and
# Kāra define it, `x * (180 / pi)`, since math.degrees divides by pi / 180
# and rounds differently.
import math

TO_DEGREES = 180.0 / math.pi


def visible_points(points, angle, location):
    here = 0
    dirs = []
    for p in points:
        dx, dy = p[0] - location[0], p[1] - location[1]
        if dx == 0 and dy == 0:
            here += 1
        else:
            dirs.append(math.atan2(dy, dx) * TO_DEGREES)
    dirs.sort()
    m = len(dirs)
    for i in range(m):
        dirs.append(dirs[i] + 360.0)
    reach = angle + 1e-9
    best = j = 0
    for i in range(len(dirs)):
        while dirs[i] - dirs[j] > reach:
            j += 1
        best = max(best, i - j + 1)
    return best + here


seed = 1610


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = seen = visible = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % most + 1
        points = []
        for _ in range(n):
            x = next_random() % (top + 1)
            y = next_random() % (top + 1)
            points.append([x, y])
        angle = next_random() % 360
        lx = next_random() % (top + 1)
        ly = next_random() % (top + 1)
        v = visible_points(points, angle, [lx, ly])
        check = mix(check, v)
        visible += v
        seen += n
    print(f"{count} problems of up to {most} points from 0 to {top}: {seen} points, {visible} visible, checksum {check}")


examples = [
    ([[2, 1], [2, 2], [3, 3]], 90, [1, 1]),
    ([[2, 1], [2, 2], [3, 4], [1, 1]], 90, [1, 1]),
    ([[1, 0], [2, 1]], 13, [1, 1]),
    ([[1, 1], [2, 2], [3, 3], [1, 2]], 0, [0, 0]),
    ([[5, 5], [5, 5]], 10, [5, 5]),
    ([[1, 0], [0, 1], [-1, 0], [0, -1], [0, 0]], 180, [0, 0]),
]
for points, angle, location in examples:
    print(visible_points(points, angle, location))
batch(3000, 6, 4)
batch(300, 1000, 100)
batch(3, 10000, 100)

# LeetCode #1610: Maximum Number of Visible Points -- the bench in Python,
# mirroring visible.kara: each direction in degrees, sorted and doubled
# with 360 more, and a window slid along it. `to_degrees` is written out
# as `x * (180 / pi)`, as Rust and Kāra define it.
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


def main():
    seed = 1610

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(20):
        points = []
        for _ in range(100000):
            x = next_random() % 101
            y = next_random() % 101
            points.append([x, y])
        angle = next_random() % 360
        lx = next_random() % 101
        ly = next_random() % 101
        problems.append((points, angle, [lx, ly]))
    check = visible = 0
    for points, angle, location in problems:
        v = visible_points(points, angle, location)
        check = (check * 31 + v + 1) % 1000000007
        visible += v
    print(f"20 problems of 100000 points from 0 to 100: {visible} visible, checksum {check}")


main()

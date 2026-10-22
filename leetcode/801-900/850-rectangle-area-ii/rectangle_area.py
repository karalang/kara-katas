# LeetCode #850: Rectangle Area II -- Python mirror of the ★ arm and its harness.
from bisect import bisect_left


def rectangle_area(rectangles):
    xs = sorted({v for r in rectangles for v in (r[0], r[2])})
    ys = sorted({v for r in rectangles for v in (r[1], r[3])})
    w = len(xs)
    h = len(ys)
    covered = [False] * (w * h)
    for r in rectangles:
        x1 = bisect_left(xs, r[0])
        x2 = bisect_left(xs, r[2])
        y1 = bisect_left(ys, r[1])
        y2 = bisect_left(ys, r[3])
        for i in range(x1, x2):
            for j in range(y1, y2):
                covered[i * h + j] = True
    area = 0
    for i in range(w - 1):
        for j in range(h - 1):
            if covered[i * h + j]:
                area += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return area % 1000000007


def show(rectangles):
    print(f"{rectangles} -> {rectangle_area(rectangles)}")


seed = 850


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_rectangle(size):
    a = next_random() % (size + 1)
    b = next_random() % (size + 1)
    c = next_random() % (size + 1)
    d = next_random() % (size + 1)
    return [min(a, b), min(c, d), max(a, b), max(c, d)]


def big():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 1000000001


def main():
    for rs in [[[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]], [[0, 0, 1000000000, 1000000000]],
               [[0, 0, 1, 1]], [[0, 0, 0, 5], [3, 3, 4, 3]], [[0, 0, 2, 2], [0, 0, 2, 2]],
               [[0, 0, 4, 4], [1, 1, 3, 3]], [[0, 0, 1, 1], [1, 0, 2, 1], [0, 1, 1, 2]],
               [[0, 1, 3, 2], [1, 0, 2, 3]], [[0, 0, 3, 3], [2, 2, 5, 5], [4, 4, 7, 7]],
               [[0, 0, 1000000000, 1], [0, 0, 1, 1000000000]],
               [[0, 0, 1000000000, 1000000000], [0, 0, 1000000000, 1000000000]]]:
        show(rs)
    nested = []
    grid = []
    strips = []
    for i in range(200):
        nested.append([i * 1000, i * 1000, 1000000000 - i * 1000, 1000000000 - i * 1000])
        grid.append([(i % 20) * 50000000, (i // 20) * 100000000, (i % 20) * 50000000 + 40000000,
                     (i // 20) * 100000000 + 90000000])
        if i < 100:
            strips.append([i * 10000000, 0, i * 10000000 + 5000000, 1000000000])
        else:
            strips.append([0, (i - 100) * 10000000, 1000000000, (i - 100) * 10000000 + 5000000])
    print(f"200 nested squares: {rectangle_area(nested)}")
    print(f"200 rectangles apart in a grid: {rectangle_area(grid)}")
    print(f"100 tall strips across 100 wide ones: {rectangle_area(strips)}")
    wide = []
    for _ in range(200):
        a = big()
        b = big()
        c = big()
        d = big()
        wide.append([min(a, b), min(c, d), max(a, b), max(c, d)])
    print(f"200 random rectangles up to 10^9: {rectangle_area(wide)}")
    small = [random_rectangle(60) for _ in range(200)]
    print(f"200 random rectangles up to 60: {rectangle_area(small)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 8
        size = 1 + next_random() % 12
        rectangles = [random_rectangle(size) for _ in range(n)]
        area = rectangle_area(rectangles)
        total += area
        check = (check * 31 + area) % 1000000007
    print(f"300 random sets: areas sum to {total}, checksum {check}")


main()

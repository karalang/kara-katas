# LeetCode #1779: Find Nearest Point That Has the Same X or Y Coordinate --
# the ★ arm in Python: one pass, keeping the nearest valid point so far.


def nearest_valid_point(x, y, points):
    best, nearest = -1, 2**31 - 1
    for i, (a, b) in enumerate(points):
        if a == x or b == y:
            d = abs(a - x) + abs(b - y)
            if d < nearest:
                nearest, best = d, i
    return best


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_points(n, side):
    points = []
    for _ in range(n):
        a = 1 + next_random() % side
        b = 1 + next_random() % side
        points.append([a, b])
    return points


def main():
    global seed
    print(f"{nearest_valid_point(3, 4, [[1, 2], [3, 1], [2, 4], [2, 3], [4, 4]])} {nearest_valid_point(3, 4, [[3, 4]])} {nearest_valid_point(3, 4, [[2, 3]])}")
    print(f"{nearest_valid_point(5, 5, [[5, 9], [1, 5], [5, 5]])} {nearest_valid_point(2, 2, [[2, 5], [5, 2]])} {nearest_valid_point(1, 1, [[2, 2], [3, 1]])} {nearest_valid_point(4, 4, [[5, 5], [4, 10]])} {nearest_valid_point(1, 1, [[2, 2], [3, 3], [4, 4]])}")
    seed = 1779
    wide = random_points(10000, 10000)
    column = [[5000, 1 + next_random() % 10000] for _ in range(10000)]
    copies = [[5000, 5001] for _ in range(10000)]
    print(f"the most: {nearest_valid_point(5000, 5000, wide)} {nearest_valid_point(5000, 5000, column)} {nearest_valid_point(5000, 5000, copies)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        side = 1 + next_random() % 6
        x = 1 + next_random() % side
        y = 1 + next_random() % side
        points = random_points(n, side)
        check = (check * 31 + nearest_valid_point(x, y, points) + 1) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()

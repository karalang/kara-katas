# LeetCode #1779: Find Nearest Point That Has the Same X or Y Coordinate --
# the bench in Python, mirroring nearest_valid_point.kara: one pass keeping
# the nearest valid point so far.


def nearest_valid_point(x, y, points):
    best, nearest = -1, 2**31 - 1
    for i in range(len(points)):
        a, b = points[i][0], points[i][1]
        if a == x or b == y:
            d = abs(a - x) + abs(b - y)
            if d < nearest:
                nearest, best = d, i
    return best


seed = 1779


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(20):
        points = []
        for _ in range(10000):
            a = 1 + next_random() % 100
            b = 1 + next_random() % 100
            points.append([a, b])
        lists.append(points)
    check = 0
    for call in range(20000):
        x = 1 + (check + call) % 100
        y = 1 + (check // 100 + call * 7) % 100
        found = nearest_valid_point(x, y, lists[call % 20])
        check = (check * 31 + found + 1) % 1000000007
    print(f"20000 calls over 20 lists: checksum {check}")


main()

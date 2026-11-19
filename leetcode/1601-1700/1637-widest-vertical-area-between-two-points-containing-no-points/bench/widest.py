# LeetCode #1637: Widest Vertical Area Between Two Points Containing No
# Points -- the bench's Python mirror: the ★ arm on 40 random sets of
# 100000 points with x and y from 0 to 10^9, all drawn first.


def max_width_of_vertical_area(points):
    xs = sorted(p[0] for p in points)
    return max(b - a for a, b in zip(xs, xs[1:]))


seed = 1637


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sets = []
    for _ in range(40):
        points = []
        for _ in range(100000):
            x = (next_random() * 32768 + next_random()) % 1000000001
            y = (next_random() * 32768 + next_random()) % 1000000001
            points.append([x, y])
        sets.append(points)
    check = 0
    total = 0
    for points in sets:
        width = max_width_of_vertical_area(points)
        total += width
        check = (check * 31 + width + 1) % 1000000007
    print(f"40 sets of 100000 points: widths sum to {total}, checksum {check}")


main()

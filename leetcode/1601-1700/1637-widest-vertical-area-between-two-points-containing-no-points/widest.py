# LeetCode #1637: Widest Vertical Area Between Two Points Containing No
# Points -- the Python mirror of the ★ arm: the x coordinates sorted, and
# the widest step between neighbours.


def max_width_of_vertical_area(points):
    xs = sorted(p[0] for p in points)
    return max(b - a for a, b in zip(xs, xs[1:]))


# ---- the harness: the same as every arm's ---------------------------------

seed = 1637


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        points = []
        for _ in range(n):
            x = (next_random() * 32768 + next_random()) % (top + 1)
            y = (next_random() * 32768 + next_random()) % (top + 1)
            points.append([x, y])
        width = max_width_of_vertical_area(points)
        total += width
        check = (check * 31 + width + 1) % 1000000007
    print(f"{count} sets of up to {most} points: widths sum to {total}, checksum {check}")


print(max_width_of_vertical_area([[8, 7], [9, 9], [7, 4], [9, 7]]))
print(max_width_of_vertical_area([[3, 1], [9, 0], [1, 0], [1, 4], [5, 3], [8, 8]]))
print(max_width_of_vertical_area([[4, 0], [4, 9]]))
print(max_width_of_vertical_area([[0, 0], [1000000000, 1000000000]]))
print(max_width_of_vertical_area([[1, 5], [2, 5], [3, 5], [90, 5]]))
batch(3000, 6, 10)
batch(300, 1000, 1000000000)
batch(5, 100000, 1000000000)

# LeetCode #2250: Count Number of Rectangles Containing Each Point -- the
# benchmark's Python mirror of rectangles.kara: rectangles bucketed by
# height, each bucket's lengths sorted, a point summing over the buckets
# of height y to 100 how many lengths are at least x (bisect_left).
from bisect import bisect_left


def count_rectangles(rectangles, points):
    by_height = [[] for _ in range(101)]
    for length, height in rectangles:
        by_height[height].append(length)
    for lengths in by_height:
        lengths.sort()
    counts = []
    for x, y in points:
        count = 0
        for h in range(y, 101):
            lengths = by_height[h]
            count += len(lengths) - bisect_left(lengths, x)
        counts.append(count)
    return counts


seed = 2250


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    check = 0
    for _ in range(4):
        rectangles = []
        for _ in range(50000):
            l = wide_random() % 1000000000 + 1
            h = next_random() % 100 + 1
            rectangles.append((l, h))
        points = []
        for _ in range(50000):
            x = wide_random() % 1000000000 + 1
            y = next_random() % 100 + 1
            points.append((x, y))
        for c in count_rectangles(rectangles, points):
            check = (check * 31 + c) % 1000000007
    print(f"4 cases of 5 * 10^4 rectangles and points: checksum {check}")


main()

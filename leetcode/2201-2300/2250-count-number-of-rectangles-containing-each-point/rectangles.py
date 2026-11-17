# LeetCode #2250: Count Number of Rectangles Containing Each Point -- the
# Python mirror of rectangles.kara: the rectangles bucketed by height,
# each bucket's lengths sorted, and a point summing over the buckets of
# height y to 100 how many lengths are at least x, by binary search.
# O(r log r + p * 100 log r).
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_pairs(count, wide, high):
    out = []
    for _ in range(count):
        a = wide_random() % wide + 1
        b = next_random() % high + 1
        out.append([a, b])
    return out


def fold_list(values):
    acc = len(values)
    for v in values:
        acc = (acc * 1009 + v) % 1000000007
    return acc


def main():
    global seed
    examples = [
        ([[1, 2], [2, 3], [2, 5]], [[2, 1], [1, 4]]),
        ([[1, 1], [2, 2], [3, 3]], [[1, 3], [1, 1]]),
        ([[5, 5]], [[5, 5]]),
        ([[5, 5]], [[6, 5], [5, 6]]),
        ([[1000000000, 100], [1, 1]], [[1000000000, 100], [1, 1]]),
        ([[3, 4], [3, 4], [3, 4]], [[3, 4], [1, 1], [4, 3]]),
    ]
    for rectangles, points in examples:
        print(f"{rectangles} {points} -> {count_rectangles(rectangles, points)}")
    seed = 2250
    total = 0
    check = 0
    for _ in range(2000):
        r = next_random() % 8 + 1
        p = next_random() % 8 + 1
        rectangles = random_pairs(r, 10, 10)
        points = random_pairs(p, 10, 10)
        counts = count_rectangles(rectangles, points)
        total += sum(counts)
        check = (check * 31 + fold_list(counts)) % 1000000007
    print(f"2000 cases: {total} in all, checksum {check}")
    rectangles = random_pairs(50000, 1000000000, 100)
    points = random_pairs(10000, 1000000000, 100)
    counts = count_rectangles(rectangles, points)
    print(f"5 * 10^4 rectangles, 10^4 points: {sum(counts)} in all, checksum {fold_list(counts)}")


main()

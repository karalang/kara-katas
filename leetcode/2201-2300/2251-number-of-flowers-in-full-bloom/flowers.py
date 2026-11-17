# LeetCode #2251: Number of Flowers in Full Bloom -- Python mirror of
# flowers.kara: the starts and the ends sorted once, and each person the
# starts of at most t less the ends before t, by bisect.
from bisect import bisect_left, bisect_right


def full_bloom_flowers(flowers, people):
    starts = sorted(f[0] for f in flowers)
    ends = sorted(f[1] for f in flowers)
    return [bisect_right(starts, t) - bisect_left(ends, t) for t in people]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def random_flowers(count, top):
    out = []
    for _ in range(count):
        a = wide_random() % top + 1
        b = wide_random() % top + 1
        out.append([min(a, b), max(a, b)])
    return out


def random_people(count, top):
    return [wide_random() % top + 1 for _ in range(count)]


def fold_list(values):
    acc = len(values)
    for v in values:
        acc = (acc * 1009 + v) % 1000000007
    return acc


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        ([[1, 6], [3, 7], [9, 12], [4, 13]], [2, 3, 7, 11]),
        ([[1, 10], [3, 3]], [3, 3, 2]),
        ([[4, 8]], [3, 4, 8, 9]),
        ([[1, 1000000000]], [1, 500000000, 1000000000]),
        ([[2, 5], [2, 5], [2, 5]], [1, 2, 5, 6]),
        ([[3, 3], [5, 5], [3, 3]], [3, 4, 5]),
    ]
    for flowers, people in examples:
        print(f"{show(flowers)} {show(people)} -> {show(full_bloom_flowers(flowers, people))}")
    seed = 2251
    total = 0
    check = 0
    for _ in range(2000):
        f = next_random() % 8 + 1
        p = next_random() % 8 + 1
        flowers = random_flowers(f, 10)
        people = random_people(p, 10)
        counts = full_bloom_flowers(flowers, people)
        total += sum(counts)
        check = (check * 31 + fold_list(counts)) % 1000000007
    print(f"2000 cases: {total} in all, checksum {check}")
    flowers = random_flowers(50000, 1000000000)
    people = random_people(50000, 1000000000)
    counts = full_bloom_flowers(flowers, people)
    print(f"5 * 10^4 flowers, 5 * 10^4 people: {sum(counts)} in all, checksum {fold_list(counts)}")


main()

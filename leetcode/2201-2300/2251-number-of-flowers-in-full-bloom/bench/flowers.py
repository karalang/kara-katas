# LeetCode #2251: Number of Flowers in Full Bloom -- the benchmark's
# Python mirror of flowers.kara: the starts and the ends sorted once, and
# each person the starts of at most t less the ends before t, by bisect.
from bisect import bisect_left, bisect_right


def full_bloom_flowers(flowers, people):
    starts = sorted(f[0] for f in flowers)
    ends = sorted(f[1] for f in flowers)
    return [bisect_right(starts, t) - bisect_left(ends, t) for t in people]


seed = 2251


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    check = 0
    for _ in range(20):
        flowers = []
        for _ in range(50000):
            a = wide_random() % 1000000000 + 1
            b = wide_random() % 1000000000 + 1
            flowers.append((min(a, b), max(a, b)))
        people = [wide_random() % 1000000000 + 1 for _ in range(50000)]
        for c in full_bloom_flowers(flowers, people):
            check = (check * 31 + c) % 1000000007
    print(f"20 cases of 5 * 10^4 flowers and people: checksum {check}")


main()

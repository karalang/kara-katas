# LeetCode #1093: Statistics from a Large Sample -- Python mirror of the ★
# arm: one walk for the smallest and largest value, the sum, the total and
# the mode, a second walk of the running total to the middle places for
# the median. Same cases and output as sample_stats.kara.


def sample_stats(count):
    low, high, s, total, mode = -1, 0, 0, 0, 0
    for k, c in enumerate(count):
        if c == 0:
            continue
        if low < 0:
            low = k
        high = k
        s += k * c
        total += c
        if c > count[mode]:
            mode = k
    left, right = (total - 1) // 2, total // 2
    seen, median_low, median_high = 0, -1, -1
    for k, c in enumerate(count):
        seen += c
        if median_low < 0 and seen > left:
            median_low = k
        if seen > right:
            median_high = k
            break
    return [float(low), float(high), s / total, (median_low + median_high) / 2.0, float(mode)]


seed = 1093


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(repr(x) for x in v) + "]"


def counts(given):
    c = [0] * 256
    for k, n in given:
        c[k] = n
    return c


def one_mode(c):
    top = max(c)
    firsts = [k for k in range(len(c)) if c[k] == top]
    if len(firsts) > 1:
        c[firsts[0]] += 1


def main():
    cases = [
        [(1, 1), (2, 3), (3, 4)],
        [(1, 4), (2, 3), (3, 2), (4, 2)],
        [(0, 1)],
        [(255, 1)],
        [(0, 1), (255, 2)],
        [(7, 1000000000)],
        [(0, 499999999), (255, 500000001)],
        [(10, 3), (20, 4), (30, 2)],
        [(5, 2), (6, 1), (9, 1)],
        [(100, 1), (101, 2), (200, 1), (201, 1)],
    ]
    for given in cases:
        print(show(sample_stats(counts(given))))
    h = modes = 0
    for i in range(2000):
        given = []
        for _ in range(next_random() % 12 + 1):
            k = next_random() % 256
            n = next_random() % 20 + 1 if i % 2 == 0 else next_random() * 50000 % 100000000 + 1
            given.append((k, n))
        c = counts(given)
        one_mode(c)
        s = sample_stats(c)
        modes += int(s[4])
        for x in s:
            h = (h * 31 + int(x * 1000000.0)) % 1000000007
    print(f"2000 random samples: modes sum to {modes}, checksum {h}")
    c = [0] * 256
    left = 1000000000
    for k in range(256):
        n = left if k == 255 else min(next_random() * 1000 % 7800000, left)
        c[k] = n
        left -= n
    one_mode(c)
    print(show(sample_stats(c)))


main()

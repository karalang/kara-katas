# LeetCode #702: Search in a Sorted Array of Unknown Size -- doubling,
# then halving.
#
# A mirror of search_in_a_sorted_array_of_unknown_size.kara (the ★ arm)
# and its harness.

seed = 0
PAST = 2147483647


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class ArrayReader:
    def __init__(self, secret):
        self.secret = secret
        self.reads = 0

    def get(self, index):
        self.reads += 1
        if index < 0 or index >= len(self.secret):
            return PAST
        return self.secret[index]


def search(reader, target):
    lo, hi = 0, 1
    while reader.get(hi) < target:
        lo = hi
        hi *= 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        v = reader.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def find(secret, target):
    return search(ArrayReader(secret), target)


def show(secret, target):
    print(f"{secret} target {target}: {find(secret, target)}")


def random_sorted(n, low, gap):
    out = []
    v = low
    while len(out) < n and v <= 10000:
        out.append(v)
        v += 1 + next_random() % gap
    return out


def main():
    global seed
    for t in (9, 2, -1, 12, -10000, 10000, 4):
        show([-1, 0, 3, 5, 9, 12], t)
    for t in (5, 4, 6):
        show([5], t)
    show([-10000, 10000], 10000)
    reader = ArrayReader([-10000 + 2 * i for i in range(10000)])
    found = total = 0
    for k in range(2858):
        at = search(reader, -10000 + 7 * k)
        if at >= 0:
            found += 1
        total = (total * 31 + at + 1) % 1000000007
    print(f"10000 values, 2858 targets: {found} found, checksum {total}")
    print(f"10000 values, last and past it: {search(reader, 9998)} {search(reader, 10000)}")
    seed = 702
    found = total = 0
    for _ in range(1000):
        n = 1 + next_random() % 300
        low = next_random() % 20001 - 10000
        gap = 1 + next_random() % 60
        secret = random_sorted(n, low, gap)
        target = next_random() % 20001 - 10000
        if next_random() % 2 == 0:
            target = secret[next_random() % len(secret)]
        at = find(secret, target)
        if at >= 0:
            found += 1
        total = (total * 31 + at + 1) % 1000000007
    print(f"1000 random arrays: {found} found, checksum {total}")


main()

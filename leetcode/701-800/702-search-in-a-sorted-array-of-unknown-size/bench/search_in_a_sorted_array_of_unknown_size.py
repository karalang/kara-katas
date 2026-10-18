# LeetCode #702: Search in a Sorted Array of Unknown Size -- bench program, Python mirror of the doubling arm.

seed = 702


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class ArrayReader:
    __slots__ = ("secret", "reads")

    def __init__(self, secret):
        self.secret = secret
        self.reads = 0

    def get(self, index):
        self.reads += 1
        if index < 0 or index >= len(self.secret):
            return 2147483647
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


def main():
    readers = []
    for _ in range(100):
        secret = []
        v = -10000
        for _ in range(10000):
            secret.append(v)
            v += 1 + next_random() % 2
        readers.append(ArrayReader(secret))
    rounds = 5
    found = 0
    checksum = 0
    for _ in range(rounds):
        for reader in readers:
            for target in range(-10000, 10001, 2):
                at = search(reader, target)
                if at >= 0:
                    found += 1
                    checksum = (checksum * 31 + at) % 1000000007
    reads = sum(r.reads for r in readers)
    print(f"{rounds} rounds of 100 arrays of 10000: {found} found, {reads} reads, checksum {checksum}")


main()

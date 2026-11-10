# LeetCode #2080: Range Frequency Queries -- Python mirror of the ★ arm's
# benchmark (frequency.kara): 10 arrays of 10^5 values, each built into a
# dict of every value's places once and then asked 1000000 queries.
from bisect import bisect_left, bisect_right

seed = 2080


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class RangeFreqQuery:
    def __init__(self, arr):
        self.places = {}
        for i, v in enumerate(arr):
            self.places.setdefault(v, []).append(i)

    def query(self, left, right, value):
        at = self.places.get(value)
        if at is None:
            return 0
        return bisect_right(at, right) - bisect_left(at, left)


def main():
    n = 100000
    total = check = 0
    for t in range(10):
        top = [100, 1000, 10000][t % 3]
        arr = [next_random() % top + 1 for _ in range(n)]
        index = RangeFreqQuery(arr)
        for _ in range(1000000):
            a = (next_random() * 32768 + next_random()) % n
            b = (next_random() * 32768 + next_random()) % n
            if next_random() % 2 == 0:
                value = arr[(next_random() * 32768 + next_random()) % n]
            else:
                value = next_random() % (top + 1) + 1
            c = index.query(min(a, b), max(a, b), value)
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"10000000 queries: sum {total}, checksum {check}")


main()

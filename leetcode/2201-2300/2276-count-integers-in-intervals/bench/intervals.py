# LeetCode #2276: Count Integers in Intervals -- the bench, the ★ arm.
# The `SortedMap` is a sorted list of starts beside a dict of ends.
from bisect import bisect_right, insort


class CountIntervals:
    def __init__(self):
        self.starts = []
        self.ends = {}
        self.total = 0

    def add(self, left, right):
        l = left
        r = right
        while True:
            i = bisect_right(self.starts, r)
            if i == 0:
                break
            a = self.starts[i - 1]
            b = self.ends[a]
            if b < l:
                break
            l = min(l, a)
            r = max(r, b)
            self.total -= b - a + 1
            del self.starts[i - 1]
            del self.ends[a]
        self.total += r - l + 1
        insort(self.starts, l)
        self.ends[l] = r

    def count(self):
        return self.total


# ---- bench harness ---------------------------------------------------------

seed = 2276


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    check = 0
    for t in range(10):
        span = 1000000000 if t % 2 == 0 else 1000000
        intervals = CountIntervals()
        for _ in range(100000):
            if next_random() % 3 == 0:
                check = (check * 31 + intervals.count()) % 1000000007
            else:
                left = wide_random() % span + 1
                right = min(left + wide_random() % 1000, 1000000000)
                intervals.add(left, right)
    print(f"10 runs of 10^5: checksum {check}")


main()

# LeetCode #715: Range Module -- a sorted list of disjoint ranges.
# Benchmark mirror of the Kara star arm: parallel sorted lists of
# starts and ends, a binary search on the ends, and inserts and removals
# that shift the rest.


class RangeModule:
    def __init__(self):
        self.starts = []
        self.ends = []

    def first_ending_after(self, x):
        lo, hi = 0, len(self.ends)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.ends[mid] > x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def add_range(self, left, right):
        i = self.first_ending_after(left - 1)
        lo, hi, j = left, right, i
        while j < len(self.starts) and self.starts[j] <= right:
            if self.starts[j] < lo:
                lo = self.starts[j]
            if self.ends[j] > hi:
                hi = self.ends[j]
            j += 1
        if j == i:
            self.starts.insert(i, lo)
            self.ends.insert(i, hi)
        else:
            self.starts[i] = lo
            self.ends[i] = hi
            for _ in range(i + 1, j):
                del self.starts[i + 1]
                del self.ends[i + 1]

    def query_range(self, left, right):
        i = self.first_ending_after(left)
        return i < len(self.starts) and self.starts[i] <= left and self.ends[i] >= right

    def remove_range(self, left, right):
        i = self.first_ending_after(left)
        if i < len(self.starts) and self.starts[i] < left:
            end = self.ends[i]
            self.ends[i] = left
            if end > right:
                self.starts.insert(i + 1, right)
                self.ends.insert(i + 1, end)
                return
            i += 1
        while i < len(self.starts) and self.starts[i] < right:
            if self.ends[i] > right:
                self.starts[i] = right
                return
            del self.starts[i]
            del self.ends[i]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_below(seed, bound):
    hi = next_random(seed)
    lo = next_random(seed)
    return (hi * 32768 + lo) % bound


def main():
    seed = [715]
    lists = []
    for _ in range(10):
        calls = []
        for _ in range(100000):
            kind = next_random(seed) % 3
            left = 1 + random_below(seed, 10000000)
            right = left + 1 + random_below(seed, 10000)
            calls.append((kind, left, right))
        lists.append(calls)
    held = 0
    for _ in range(10):
        for calls in lists:
            m = RangeModule()
            for kind, left, right in calls:
                if kind == 0:
                    m.add_range(left, right)
                elif kind == 1:
                    m.remove_range(left, right)
                elif m.query_range(left, right):
                    held += 1
    print(f"10 rounds of 10 lists of 100000 calls: {held} queries held")


main()

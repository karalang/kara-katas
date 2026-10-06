# Bench mirror of summary_ranges.kara (the sorted-vector arm), same algorithm.


class SummaryRanges:
    def __init__(self):
        self.starts = []
        self.ends = []

    def first_after(self, value):
        lo, hi = 0, len(self.starts)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.starts[mid] <= value:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def add_num(self, value):
        i = self.first_after(value)
        joins_left = i > 0 and self.ends[i - 1] >= value - 1
        if i > 0 and self.ends[i - 1] >= value:
            return
        joins_right = i < len(self.starts) and self.starts[i] == value + 1
        if joins_left and joins_right:
            self.ends[i - 1] = self.ends[i]
            del self.starts[i]
            del self.ends[i]
        elif joins_left:
            self.ends[i - 1] = value
        elif joins_right:
            self.starts[i] = value
        else:
            self.starts.insert(i, value)
            self.ends.insert(i, value)

    def get_intervals(self):
        return [(self.starts[i], self.ends[i]) for i in range(len(self.starts))]


def main():
    rounds = 150
    sink = 0
    for r in range(rounds):
        stream = SummaryRanges()
        state = 352 + r
        for i in range(1, 30001):
            state = (state * 1103515245 + 12345) % 2147483648
            stream.add_num((state >> 8) % 10001)
            if i % 3000 == 0:
                for s, e in stream.get_intervals():
                    sink = (sink * 31 + s * 7 + e + r) % 1000000007
    print(f"sink {sink}")


main()

# LeetCode #352: Data Stream as Disjoint Intervals — Python mirror of
# summary_ranges.kara (a sorted list of starts with bisect stands in for the
# sorted map; the floor/ceiling logic is the same).
import bisect


class SummaryRanges:
    def __init__(self):
        self.keys = []   # interval starts, sorted
        self.end = {}    # start -> end

    def add_num(self, value):
        start, end = value, value
        i = bisect.bisect_right(self.keys, value) - 1
        if i >= 0:
            s = self.keys[i]
            e = self.end[s]
            if e >= value:
                return
            if e == value - 1:
                start = s
        j = bisect.bisect_left(self.keys, value + 1)
        if j < len(self.keys) and self.keys[j] == value + 1:
            s = self.keys[j]
            end = self.end.pop(s)
            self.keys.pop(j)
        if start not in self.end:
            bisect.insort(self.keys, start)
        self.end[start] = end

    def get_intervals(self):
        return [(s, self.end[s]) for s in self.keys]


def show(intervals):
    if not intervals:
        return "(empty)"
    return " ".join(f"[{s}, {e}]" for s, e in intervals)


def main():
    ranges = SummaryRanges()
    for v in [1, 3, 7, 2, 6]:
        ranges.add_num(v)
        print(f"add {v}: {show(ranges.get_intervals())}")

    edge = SummaryRanges()
    print(f"nothing added: {show(edge.get_intervals())}")
    for v in [5, 5, 0, 10000, 3, 4, 9999, 9998, 2, 1, 6]:
        edge.add_num(v)
    print(f"edges: {show(edge.get_intervals())}")

    stream = SummaryRanges()
    state = 352
    checksum = 0
    for i in range(1, 30001):
        state = (state * 1103515245 + 12345) % 2147483648
        stream.add_num((state >> 8) % 10001)
        if i % 3000 == 0:
            intervals = stream.get_intervals()
            covered = 0
            for s, e in intervals:
                covered += e - s + 1
                checksum = (checksum * 31 + s * 7 + e) % 1000000007
            print(f"after {i}: {len(intervals)} intervals covering {covered}")
    print(f"checksum {checksum}")


main()

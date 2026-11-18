# LeetCode #2276: Count Integers in Intervals -- the Python mirror of the
# ★ arm, `intervals.kara`, line for line. Its output is byte-identical.
# The `SortedMap` is a sorted list of starts beside a dict of ends, and
# `floor` a `bisect`.
from bisect import bisect_right, insort


class CountIntervals:
    def __init__(self):
        self.starts = []
        self.ends = {}
        self.total = 0

    def floor(self, key):
        i = bisect_right(self.starts, key)
        if i == 0:
            return None
        a = self.starts[i - 1]
        return a, self.ends[a]

    def add(self, left, right):
        l = left
        r = right
        while True:
            found = self.floor(r)
            if found is None:
                break
            a, b = found
            if b < l:
                break
            l = min(l, a)
            r = max(r, b)
            self.total -= b - a + 1
            self.starts.remove(a)
            del self.ends[a]
        self.total += r - l + 1
        insort(self.starts, l)
        self.ends[l] = r

    def count(self):
        return self.total


def play(calls):
    intervals = CountIntervals()
    answers = []
    for left, right in calls:
        if left == 0:
            answers.append(intervals.count())
        else:
            intervals.add(left, right)
    return answers


seed = 2276


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def make_calls(m, span, long):
    out = []
    for _ in range(m):
        if next_random() % 3 == 0:
            out.append((0, 0))
        else:
            left = wide_random() % span + 1
            right = min(left + wide_random() % long, 1000000000)
            out.append((left, right))
    return out


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        [(2, 3), (7, 10), (0, 0), (5, 8), (0, 0)],
        [(1, 10), (3, 4), (0, 0)],
        [(1, 2), (3, 4), (0, 0)],
        [(5, 5), (5, 5), (0, 0)],
        [(1, 2), (5, 6), (0, 0), (3, 4), (0, 0), (1, 6), (0, 0)],
        [(1, 1000000000), (0, 0)],
    ]
    for calls in examples:
        print(f"{show(calls)} -> {show(play(calls))}")
    check = 0
    for t in range(1000):
        m = next_random() % 40 + 1
        run = make_calls(m, [10, 100, 1000000000][t % 3], [3, 30, 1000000000][t // 3 % 3])
        for a in play(run):
            check = (check * 31 + a % 1000000007) % 1000000007
    print(f"1000 runs: checksum {check}")
    lasts = []
    for span, long in [(1000000000, 1000), (1000000, 1000)]:
        answers = play(make_calls(10000, span, long))
        lasts.append(answers[-1])
    print(f"10^4 calls: last counts {show(lasts)}")


main()

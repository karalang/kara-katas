# LeetCode #715: Range Module -- a sorted list of disjoint ranges.
#
# A mirror of range_module.kara (the ★ arm) and its harness.


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
            lo = min(lo, self.starts[j])
            hi = max(hi, self.ends[j])
            j += 1
        if j == i:
            self.starts.insert(i, lo)
            self.ends.insert(i, hi)
        else:
            self.starts[i] = lo
            self.ends[i] = hi
            del self.starts[i + 1:j]
            del self.ends[i + 1:j]

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


def run(calls):
    m = RangeModule()
    answers = []
    for kind, left, right in calls:
        if kind == 0:
            m.add_range(left, right)
        elif kind == 1:
            m.remove_range(left, right)
        else:
            answers.append(m.query_range(left, right))
    return answers


def random_calls(seed, count, top, longest):
    calls = []
    for _ in range(count):
        kind = next_random(seed) % 3
        left = 1 + random_below(seed, top)
        right = left + 1 + random_below(seed, longest)
        if right > 1000000000:
            right = 1000000000
        if left < right:
            calls.append((kind, left, right))
    return calls


def show(answers):
    print("[" + ", ".join("true" if a else "false" for a in answers) + "]")


def summary(name, answers):
    held = 0
    total = 0
    for a in answers:
        bit = 1 if a else 0
        held += bit
        total = (total * 131 + bit + 1) % 1000000007
    print(f"{name}: {len(answers)} queries, {held} held, checksum {total}")


def main():
    show(run([(0, 10, 20), (1, 14, 16), (2, 10, 14), (2, 13, 15), (2, 16, 17)]))
    show(run([(0, 1, 3), (0, 3, 5), (2, 1, 5), (1, 2, 3), (2, 1, 5), (2, 1, 2), (2, 3, 5), (2, 2, 3)]))
    show(run([(0, 1, 10), (1, 1, 2), (1, 9, 10), (2, 2, 9), (2, 1, 3), (2, 8, 10), (1, 5, 6), (2, 2, 5), (2, 5, 7), (2, 6, 9)]))
    show(run([(0, 1, 2), (0, 3, 4), (0, 5, 6), (0, 7, 8), (2, 1, 8), (0, 2, 7), (2, 1, 8), (2, 1, 9)]))
    show(run([(0, 5, 10), (1, 1, 4), (1, 11, 20), (2, 5, 10), (1, 1, 20), (2, 5, 6), (0, 1, 2), (2, 1, 2), (2, 1, 3)]))
    show(run([(2, 1, 2), (1, 1, 2), (0, 4, 6), (0, 1, 3), (2, 1, 6), (0, 3, 4), (2, 1, 6), (1, 3, 4), (2, 1, 3), (2, 4, 6)]))
    show(run([(0, 1, 1000000000), (2, 1, 1000000000), (1, 500000000, 500000001), (2, 1, 500000000), (2, 499999999, 500000002), (2, 500000001, 1000000000)]))
    seed = [715]
    summary("10000 calls up to 10^9", run(random_calls(seed, 10000, 999999999, 1000000000)))
    summary("10000 calls up to 100", run(random_calls(seed, 10000, 100, 20)))
    summary("10000 short calls up to 10^6", run(random_calls(seed, 10000, 1000000, 1000)))
    summary("10000 calls up to 10^9 of up to 10^6", run(random_calls(seed, 10000, 999999999, 1000000)))


main()

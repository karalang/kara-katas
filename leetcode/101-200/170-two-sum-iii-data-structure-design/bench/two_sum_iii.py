"""Benchmark workload for LeetCode #170 — Two Sum III (Python; scale lane)."""


class TwoSum:
    def __init__(self):
        self.counts = {}


def add(ds, number):
    ds.counts[number] = ds.counts.get(number, 0) + 1


def find(ds, value):
    found = False
    counts = ds.counts
    for k in counts:
        complement = value - k
        if complement == k:
            if counts[k] >= 2:
                found = True
        else:
            if complement in counts:
                found = True
    return found


def main():
    k_range = 6000
    n_add = 170
    m_query = 1200000

    ds = TwoSum()
    state = 12345
    for _ in range(n_add):
        state = (state * 1103515245 + 12345) & 2147483647
        add(ds, state % k_range)

    sink = 0
    for _ in range(m_query):
        state = (state * 1103515245 + 12345) & 2147483647
        target = state % (2 * k_range)
        if find(ds, target):
            sink += 1
    print(sink)


main()

"""LeetCode 295 — Find Median from Data Stream (two heaps).

Mirror of median_finder.kara: same algorithm, same output. Python's heapq is a
MIN-heap only, so the lower half is negated to make a max-heap — the trick the
Kara version deliberately avoids (see its header: -i64.MIN overflows, and Kara
traps that). Python's ints are unbounded, so the negation is safe here; the
difference is a property of the languages, not of the algorithm.
"""

import heapq


class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap via negation: lower half
        self.hi = []  # min-heap: upper half

    def add(self, v):
        heapq.heappush(self.lo, -v)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


def fmt(x):
    """Match Kara/Rust shortest-representation float Display: 2.0 prints as 2."""
    return f"{x:g}"


def main():
    mf = MedianFinder()
    for v in [1, 3, 2, 4, 0, 9, 7]:
        mf.add(v)
        print(f"add {v} -> median {fmt(mf.median())}")


if __name__ == "__main__":
    main()

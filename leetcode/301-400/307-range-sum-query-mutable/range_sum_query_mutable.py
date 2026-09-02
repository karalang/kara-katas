"""LeetCode 307 - Range Sum Query, Mutable.

Mirror of range_sum_query_mutable.kara: a Fenwick tree (binary indexed tree),
1-indexed internally, absorbing a delta on write and gathering disjoint slots
on read. lowbit(x) = x & -x is the value of x's lowest set bit; the two walks
are opposite directions over it.
"""


class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.n = len(nums)
        self.tree = [0] * (self.n + 1)
        self.data = [0] * self.n
        for i, v in enumerate(nums):
            self.update(i, v)

    def add(self, i: int, delta: int) -> None:
        """Fold delta into every slot covering index i, climbing by lowbit."""
        x = i + 1
        while x <= self.n:
            self.tree[x] += delta
            x += x & -x

    def update(self, i: int, val: int) -> None:
        delta = val - self.data[i]
        self.data[i] = val
        self.add(i, delta)

    def prefix(self, i: int) -> int:
        """Sum of [0, i), gathered from the disjoint slots that tile it."""
        total = 0
        x = i
        while x > 0:
            total += self.tree[x]
            x -= x & -x
        return total

    def sum_range(self, left: int, right: int) -> int:
        return self.prefix(right + 1) - self.prefix(left)


def report(nums: list[int], ops: list[int]) -> None:
    """`ops` is a flat list of (kind, a, b) triples: 0 = update, 1 = sum_range."""
    st = NumArray(list(nums))
    parts = []
    for k in range(0, len(ops) - 2, 3):
        kind, a, b = ops[k], ops[k + 1], ops[k + 2]
        if kind == 0:
            st.update(a, b)
            parts.append(f"u({a},{b})")
        else:
            parts.append(str(st.sum_range(a, b)))
    body = ", ".join(str(v) for v in nums)
    print(f"[{body}] -> " + " ".join(parts))


def main() -> None:
    # The example from the LeetCode statement.
    report([1, 3, 5], [1, 0, 2, 0, 1, 2, 1, 0, 2])
    # Every single-element read, before and after a write.
    report([2, 7, 4], [1, 0, 0, 1, 1, 1, 1, 2, 2, 0, 1, 9, 1, 1, 1, 1, 0, 2])
    # One element.
    report([42], [1, 0, 0, 0, 0, -5, 1, 0, 0])
    # Writing the value that is already there must change nothing.
    report([4, 4, 4, 4], [1, 0, 3, 0, 2, 4, 1, 0, 3, 1, 2, 2])
    # Negatives, and a write that flips a sign.
    report([-1, -2, -3, -4], [1, 0, 3, 1, 1, 2, 0, 0, 10, 1, 0, 3, 1, 0, 0])
    # Every prefix of a longer array, then a write in the middle.
    report([5, 1, 8, 2, 9, 3],
           [1, 0, 0, 1, 0, 1, 1, 0, 2, 1, 0, 3, 1, 0, 4, 1, 0, 5,
            0, 3, 100, 1, 0, 5, 1, 3, 3, 1, 4, 5])
    # Large magnitudes that cancel.
    report([100000, -100000, 100000], [1, 0, 2, 0, 1, 100000, 1, 0, 2, 1, 1, 1])
    # A power-of-two length, where the Fenwick and segment trees are widest.
    report([1, 2, 3, 4, 5, 6, 7, 8], [1, 0, 7, 0, 7, 0, 1, 0, 7, 1, 7, 7, 1, 4, 6])


if __name__ == "__main__":
    main()

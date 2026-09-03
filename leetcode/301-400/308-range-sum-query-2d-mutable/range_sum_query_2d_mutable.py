"""LeetCode 308 - Range Sum Query 2D, Mutable.

Mirror of range_sum_query_2d_mutable.kara: a 2D Fenwick tree (a BIT of BITs),
1-indexed in both dimensions. A write climbs the lowbit in both dimensions to
reach every slot covering its cell; a prefix read descends in both to gather
the disjoint slots tiling the origin-rectangle. The query is the four-term
inclusion-exclusion over four such prefixes.
"""


class NumMatrix:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.h = len(matrix)
        self.w = len(matrix[0]) if self.h else 0
        self.tree = [0] * ((self.h + 1) * (self.w + 1))
        self.data = [0] * (self.h * self.w)
        for r in range(self.h):
            for c in range(self.w):
                self.update(r, c, matrix[r][c])

    def add(self, r: int, c: int, delta: int) -> None:
        """Fold delta into every slot covering (r, c) — a climb in both dims."""
        stride = self.w + 1
        x = r + 1
        while x <= self.h:
            y = c + 1
            while y <= self.w:
                self.tree[x * stride + y] += delta
                y += y & -y
            x += x & -x

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.data[row * self.w + col]
        self.data[row * self.w + col] = val
        self.add(row, col, delta)

    def prefix(self, r: int, c: int) -> int:
        """Sum of the origin-rectangle [0, r) x [0, c) — a descent in both."""
        stride = self.w + 1
        total = 0
        x = r
        while x > 0:
            y = c
            while y > 0:
                total += self.tree[x * stride + y]
                y -= y & -y
            x -= x & -x
        return total

    def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (self.prefix(row2 + 1, col2 + 1)
                - self.prefix(row1, col2 + 1)
                - self.prefix(row2 + 1, col1)
                + self.prefix(row1, col1))


def matrix_of(flat: list[int], w: int) -> list[list[int]]:
    return [flat[i:i + w] for i in range(0, len(flat), w)]


def report(flat: list[int], w: int, ops: list[int]) -> None:
    """`ops` is a flat list of (kind, a, b, c, d) 5-tuples."""
    m = matrix_of(flat, w)
    st = NumMatrix(m)
    parts = []
    for k in range(0, len(ops) - 4, 5):
        kind, a, b, c, d = ops[k], ops[k + 1], ops[k + 2], ops[k + 3], ops[k + 4]
        if kind == 0:
            st.update(a, b, c)
            parts.append(f"u({a},{b},{c})")
        else:
            parts.append(str(st.sum_region(a, b, c, d)))
    print(f"{len(m)}x{w} -> " + " ".join(parts))


def main() -> None:
    # The matrix from the LeetCode statement.
    report([3, 0, 1, 4, 2,
            5, 6, 3, 2, 1,
            1, 2, 0, 1, 5,
            4, 1, 0, 1, 7,
            1, 0, 3, 0, 5], 5,
           [1, 2, 1, 4, 3, 0, 3, 2, 2, 0, 1, 2, 1, 4, 3,
            1, 0, 0, 4, 4, 1, 1, 1, 2, 2])
    # A single cell, written and re-read.
    report([42], 1, [1, 0, 0, 0, 0, 0, 0, 0, -5, 0, 1, 0, 0, 0, 0])
    # One row and one column of the same values.
    report([1, 2, 3, 4], 4, [1, 0, 0, 0, 3, 0, 0, 2, 10, 0, 1, 0, 0, 0, 3, 1, 0, 2, 0, 2])
    report([1, 2, 3, 4], 1, [1, 0, 0, 3, 0, 0, 2, 0, 10, 0, 1, 0, 0, 3, 0, 1, 2, 0, 2, 0])
    # Writing the value already present must change nothing.
    report([4, 4, 4, 4], 2, [1, 0, 0, 1, 1, 0, 1, 1, 4, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1])
    # All negative, then a write that flips a sign.
    report([-1, -2, -3,
            -4, -5, -6,
            -7, -8, -9], 3,
           [1, 0, 0, 2, 2, 1, 1, 1, 2, 2, 0, 0, 0, 100, 0, 1, 0, 0, 2, 2, 1, 0, 0, 0, 0])
    # Every cell of a 2x3 written in turn.
    report([0, 0, 0,
            0, 0, 0], 3,
           [0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 1, 2, 5, 0, 1, 0, 0, 1, 2,
            0, 0, 2, 3, 0, 1, 0, 0, 1, 2, 1, 0, 1, 1, 2])
    # Large magnitudes that cancel.
    report([100000, -100000,
            -100000, 100000], 2,
           [1, 0, 0, 1, 1, 0, 0, 1, 100000, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1])


if __name__ == "__main__":
    main()

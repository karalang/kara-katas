"""LeetCode 304 - Range Sum Query 2D, Immutable.

Mirror of range_sum_query_2d.kara: the same 2D prefix table carrying a zero
row and a zero column, so that sum_region is one four-term inclusion-exclusion
with no special case at row 0 or column 0.
"""


class NumMatrix:
    """pre[r][c] is the sum of every cell strictly above and left of (r, c)."""

    def __init__(self, matrix: list[list[int]]) -> None:
        h = len(matrix)
        w = len(matrix[0]) if h else 0
        pre = [[0] * (w + 1) for _ in range(h + 1)]
        for r in range(h):
            for c in range(w):
                # above + left - overlap + self
                pre[r + 1][c + 1] = (pre[r][c + 1] + pre[r + 1][c]
                                     - pre[r][c] + matrix[r][c])
        self.pre = pre

    def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (self.pre[row2 + 1][col2 + 1]
                - self.pre[row1][col2 + 1]
                - self.pre[row2 + 1][col1]
                + self.pre[row1][col1])


def matrix_of(flat: list[int], w: int) -> list[list[int]]:
    return [flat[i:i + w] for i in range(0, len(flat), w)]


def report(flat: list[int], w: int, qs: list[int]) -> None:
    """`qs` is a flat list of (r1, c1, r2, c2) quadruples."""
    m = matrix_of(flat, w)
    nm = NumMatrix(m)
    parts = []
    for q in range(0, len(qs) - 3, 4):
        r1, c1, r2, c2 = qs[q], qs[q + 1], qs[q + 2], qs[q + 3]
        parts.append(f"[{r1},{c1},{r2},{c2}]={nm.sum_region(r1, c1, r2, c2)}")
    print(f"{len(m)}x{w} -> " + " ".join(parts))


def main() -> None:
    # The matrix from the LeetCode statement.
    report([3, 0, 1, 4, 2,
            5, 6, 3, 2, 1,
            1, 2, 0, 1, 5,
            4, 1, 0, 1, 7,
            1, 0, 3, 0, 5], 5,
           [2, 1, 4, 3, 1, 1, 2, 2, 1, 2, 2, 4, 0, 0, 4, 4, 0, 0, 0, 0])
    # A single cell.
    report([7], 1, [0, 0, 0, 0])
    # One row, and the same values as one column.
    report([1, 2, 3, 4, 5], 5, [0, 0, 0, 4, 0, 1, 0, 3, 0, 2, 0, 2])
    report([1, 2, 3, 4, 5], 1, [0, 0, 4, 0, 1, 0, 3, 0, 2, 0, 2, 0])
    # All negative — sign errors are invisible on non-negative data.
    report([-1, -2, -3,
            -4, -5, -6,
            -7, -8, -9], 3,
           [0, 0, 2, 2, 1, 1, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2])
    # Every answer zero.
    report([0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0], 4, [0, 0, 2, 3, 1, 1, 1, 2])
    # Large magnitudes that cancel.
    report([100000, -100000, 100000,
            -100000, 100000, -100000], 3,
           [0, 0, 1, 2, 0, 0, 0, 2, 1, 0, 1, 2])


if __name__ == "__main__":
    main()

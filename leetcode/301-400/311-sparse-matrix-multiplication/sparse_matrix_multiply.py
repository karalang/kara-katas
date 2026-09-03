"""LeetCode 311 - Sparse Matrix Multiplication.

Mirror of sparse_matrix_multiply.kara: the loops reordered (i, k, j) so the
zero test lifts out of the innermost loop. A single zero in A then skips an
entire row of B, and the inner loop walks B[k] along contiguous memory.
"""


def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    m = len(a)
    k_dim = len(a[0]) if m else 0
    n = len(b[0]) if b else 0
    c = [[0] * n for _ in range(m)]
    for i in range(m):
        for k in range(k_dim):
            av = a[i][k]
            # One zero in A skips an entire row of B.
            if av != 0:
                for j in range(n):
                    c[i][j] += av * b[k][j]
    return c


def matrix_of(flat: list[int], w: int) -> list[list[int]]:
    return [flat[i:i + w] for i in range(0, len(flat), w)]


def report(a_flat: list[int], ak: int, b_flat: list[int], bn: int) -> None:
    c = multiply(matrix_of(a_flat, ak), matrix_of(b_flat, bn))
    body = " ".join("[" + ",".join(str(v) for v in row) + "]" for row in c)
    print(f"[{body}]")


def main() -> None:
    # The example from the LeetCode statement.
    report([1, 0, 0, -1, 0, 3], 3, [7, 0, 0, 0, 0, 0, 0, 0, 1], 3)
    # 1x1 identities and zeros.
    report([5], 1, [3], 1)
    report([0], 1, [9], 1)
    # A row vector times a column vector — a 1x1 dot product.
    report([1, 2, 3], 3, [4, 5, 6], 1)
    # A column vector times a row vector — a full 3x3 outer product.
    report([1, 2, 3], 1, [4, 5, 6], 3)
    # Multiplying by the identity returns the original.
    report([2, 0, 7, 0, 3, 0], 3, [1, 0, 0, 0, 1, 0, 0, 0, 1], 3)
    # An all-zero left operand annihilates whatever is on the right.
    report([0, 0, 0, 0], 2, [9, 8, 7, 6], 2)
    # Entirely dense, so every arm's zero-skipping is inert.
    report([1, 2, 3, 4], 2, [5, 6, 7, 8], 2)
    # Negative entries, and a column of B that is entirely zero.
    report([-1, 2, 3, -4], 2, [5, 0, -7, 0], 2)
    # Rectangular: 3x2 times 2x4.
    report([1, 0, 0, 2, 3, 4], 2, [1, 0, 0, 5, 0, 6, 0, 0], 4)


if __name__ == "__main__":
    main()

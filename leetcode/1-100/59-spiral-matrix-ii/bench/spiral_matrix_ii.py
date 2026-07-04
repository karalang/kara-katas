"""Benchmark workload — Spiral Matrix II (LeetCode #59).

Python mirror of bench/spiral_matrix_ii.kara. Same M=9 rotated sizes
(n=12..20), boundary-shrinking generator over a list-of-lists, position-
weighted checksum, and sink. CPython is multi-second per sample at K=180k, so
this mirror runs K=18_000 (1/10th); K is a multiple of 90 so each of the 9
sizes is hit exactly 2_000 times and the sink is exactly 1/10th of the
compiled mirrors' sink — the README quotes the projected ratio.
"""


def generate_matrix(n: int) -> list[list[int]]:
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    v = 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            grid[top][c] = v
            v += 1
        top += 1

        for r in range(top, bottom + 1):
            grid[r][right] = v
            v += 1
        right -= 1

        if top <= bottom:
            for c in range(right, left - 1, -1):
                grid[bottom][c] = v
                v += 1
            bottom -= 1

        if left <= right:
            for r in range(bottom, top - 1, -1):
                grid[r][left] = v
                v += 1
            left += 1

    return grid


def checksum(grid: list[list[int]], n: int) -> int:
    s = 0
    for i in range(n):
        for j in range(n):
            s += grid[i][j] * (i * n + j + 1)
    return s


def main() -> None:
    m_sizes = 9
    k_iters = 18_000

    total = 0
    for k in range(k_iters):
        n = 12 + (k % m_sizes)
        g = generate_matrix(n)
        total += checksum(g, n)
    print(total)


if __name__ == "__main__":
    main()

"""LeetCode #59: Spiral Matrix II — boundary shrinking, O(n²).

Mirror of spiral_matrix_ii.kara: same four-boundary ring fill with the two
guards on the bottom row / left column, same output format (n on its own
line, then each row as space-joined values with a trailing space) so the two
files diff line-for-line.
"""


def generate_matrix(n: int) -> list[list[int]]:
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    v = 1

    while top <= bottom and left <= right:
        # Top row, left → right.
        for c in range(left, right + 1):
            grid[top][c] = v
            v += 1
        top += 1

        # Right column, top → bottom.
        for r in range(top, bottom + 1):
            grid[r][right] = v
            v += 1
        right -= 1

        # Bottom row, right → left — only if a row remains.
        if top <= bottom:
            for c in range(right, left - 1, -1):
                grid[bottom][c] = v
                v += 1
            bottom -= 1

        # Left column, bottom → top — only if a column remains.
        if left <= right:
            for r in range(bottom, top - 1, -1):
                grid[r][left] = v
                v += 1
            left += 1

    return grid


def report(n: int) -> None:
    g = generate_matrix(n)
    print(n)
    for row in g:
        line = ""
        for x in row:
            line = f"{line}{x} "
        print(line)


def main() -> None:
    report(1)  # [[1]]
    report(2)  # [[1,2],[4,3]]
    report(3)  # [[1,2,3],[8,9,4],[7,6,5]]
    report(4)
    report(5)


if __name__ == "__main__":
    main()

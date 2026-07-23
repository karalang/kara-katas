"""LeetCode 221 — Maximal Square (Python mirror / oracle).

DP: dp[i][j] = side of the largest all-ones square ending at (i,j) =
1 + min(top, left, diag) when the cell is 1. Answer is max side squared.
Mirrors the Kara version.
"""


def maximal_square(grid):
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    if cols == 0:
        return 0

    dp = [[0] * cols for _ in range(rows)]
    best = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                if dp[i][j] > best:
                    best = dp[i][j]
    return best * best


def report(grid):
    print(maximal_square(grid))


def main():
    report([[1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0]])
    report([[0, 1], [1, 0]])
    report([[0]])
    report([[1]])
    report([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    report([[0, 0, 0], [0, 0, 0]])
    report([[1, 1, 0, 1],
            [1, 1, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1]])


main()

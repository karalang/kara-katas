"""LeetCode #64: Minimum Path Sum — one rolling row of DP, O(m*n) time, O(n) space.

Mirror of minimum_path_sum.kara: roll the 2-D best-cost table onto a single array
spanning the columns, updated left to right so dp[c] = grid[i][c] + min(dp[c], dp[c-1])
takes the cheaper of the cell above (old dp[c]) and the cell to the left (updated
dp[c-1]). The min replaces #62/#63's sum — per-cell costs, minimise instead of
count. Same twelve cases and the same output shape (one answer per line, then a
`sums:` fold) so the files diff line-for-line.
"""

from __future__ import annotations


def min_path_sum(grid: list[list[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    dp = [0] * cols
    dp[0] = grid[0][0]
    for j in range(1, cols):  # top row: prefix sums (left-only in-neighbour)
        dp[j] = dp[j - 1] + grid[0][j]

    for i in range(1, rows):
        dp[0] += grid[i][0]  # left column: above-only in-neighbour
        for c in range(1, cols):
            dp[c] = grid[i][c] + min(dp[c], dp[c - 1])
    return dp[cols - 1]


def report(grid: list[list[int]], acc: list[str]) -> None:
    ans = min_path_sum(grid)
    print(ans)
    acc.append(str(ans))


def main() -> None:
    acc: list[str] = []
    report([[1, 3, 1], [1, 5, 1], [4, 2, 1]], acc)   # 7
    report([[1, 2, 3], [4, 5, 6]], acc)              # 12
    report([[5]], acc)                               # 5
    report([[1, 2, 3, 4]], acc)                      # 10
    report([[1], [2], [3]], acc)                     # 6
    report([[1, 2], [1, 1]], acc)                    # 3
    report([[0, 0, 0], [0, 0, 0], [0, 0, 0]], acc)   # 0
    report([[1, 9, 9], [1, 9, 9], [1, 1, 1]], acc)   # 5
    report([[1, 3, 1, 2],                            # 9
            [2, 1, 3, 1],
            [3, 2, 1, 4],
            [1, 1, 1, 1]], acc)
    report([[200, 200], [200, 200]], acc)            # 600
    report([[7], [3], [9], [1], [5]], acc)           # 25
    report([[2, 2, 2, 2, 2, 2]], acc)                # 12
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()

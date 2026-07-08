"""LeetCode #63: Unique Paths II — one rolling row of DP, O(m*n) time, O(n) space.

Mirror of unique_paths_ii.kara: roll the 2-D obstacle-aware path-count table
onto a single array spanning the columns, updated left to right so dp[c] += dp[c-1]
combines the cell above (old dp[c]) with the cell to the left (updated dp[c-1]) —
except at an obstacle, where dp[c] is forced to 0. Obstacles break the axis
symmetry #62 exploits, so the array spans the real column count n (no swap to the
smaller side). Same thirteen cases and the same output shape (one answer per line,
then a `sums:` fold) so the files diff line-for-line.
"""

from __future__ import annotations


def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    dp = [0] * cols
    dp[0] = 1  # single virtual path entering the top-left
    for i in range(rows):
        for c in range(cols):
            if grid[i][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[cols - 1]


def report(grid: list[list[int]], acc: list[str]) -> None:
    ans = unique_paths_with_obstacles(grid)
    print(ans)
    acc.append(str(ans))


def main() -> None:
    acc: list[str] = []
    report([[0, 0, 0], [0, 1, 0], [0, 0, 0]], acc)   # 2
    report([[0, 1], [0, 0]], acc)                    # 1
    report([[0]], acc)                               # 1
    report([[1]], acc)                               # 0
    report([[1, 0], [0, 0]], acc)                    # 0
    report([[0, 0], [0, 1]], acc)                    # 0
    report([[0, 0], [1, 1], [0, 0]], acc)            # 0
    report([[0, 0, 0], [0, 0, 0], [0, 0, 0]], acc)   # 6
    report([[0, 0, 0, 0, 0, 0, 0],                   # 28
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]], acc)
    report([[0, 0, 0, 0, 0],                         # 8
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0]], acc)
    report([[0, 0, 0, 0, 0]], acc)                   # 1
    report([[0, 0, 1, 0, 0]], acc)                   # 0
    report([[0, 0, 0, 0, 0],                         # 15
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0]], acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()

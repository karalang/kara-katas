"""LeetCode #62: Unique Paths — one rolling row of DP, O(m*n) time, O(min(m,n)) space.

Mirror of unique_paths.kara: roll the 2-D path-count table onto a single array
spanning the smaller dimension, updated left to right so dp[j] += dp[j-1]
combines the cell above (old dp[j]) with the cell to the left (updated dp[j-1]).
Same ten cases and the same output shape (one answer per line, then a `sums:`
fold) so the two files diff line-for-line.
"""

from __future__ import annotations


def unique_paths(m: int, n: int) -> int:
    # Symmetric in its axes, so span the smaller side: O(min(m, n)) space.
    rows, cols = m, n
    if cols > rows:
        rows, cols = cols, rows

    dp = [1] * cols  # top row: one path (all rights) to every cell
    for _ in range(1, rows):
        for c in range(1, cols):
            dp[c] += dp[c - 1]
    return dp[cols - 1]


def report(m: int, n: int, acc: list[str]) -> None:
    ans = unique_paths(m, n)
    print(ans)
    acc.append(str(ans))


def main() -> None:
    acc: list[str] = []
    report(3, 7, acc)     # 28
    report(3, 2, acc)     # 3
    report(1, 1, acc)     # 1
    report(1, 10, acc)    # 1
    report(10, 1, acc)    # 1
    report(2, 2, acc)     # 2
    report(3, 3, acc)     # 6
    report(7, 3, acc)     # 28
    report(10, 10, acc)   # 48620
    report(51, 9, acc)    # 1916797311
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()

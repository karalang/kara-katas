"""LeetCode #72: Edit Distance — full 2-D DP table, O(m*n) time and space.

Mirror of edit_distance.kara: dp[i][j] is the Levenshtein distance between the
first i chars of a and the first j of b; a free match carries the diagonal,
otherwise 1 + min(replace, delete, insert). Borders dp[i][0]=i, dp[0][j]=j; the
answer is dp[m][n]. Same thirteen cases and the same output shape (one
edit("a","b") = d per line, then a `sums:` fold) so the files diff line-for-line.
(The rolling variant lives only in Kāra; this mirror tracks the ★.)
"""

from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if a[r - 1] == b[c - 1]:
                dp[r][c] = dp[r - 1][c - 1]
            else:
                dp[r][c] = 1 + min(dp[r - 1][c - 1], dp[r - 1][c], dp[r][c - 1])
    return dp[m][n]


def report(a: str, b: str, acc: list[str]) -> None:
    d = edit_distance(a, b)
    print(f'edit("{a}","{b}") = {d}')
    acc.append(str(d))


def main() -> None:
    acc: list[str] = []
    report("horse", "ros", acc)
    report("intention", "execution", acc)
    report("", "", acc)
    report("", "abc", acc)
    report("abc", "", acc)
    report("abc", "abc", acc)
    report("a", "b", acc)
    report("kitten", "sitting", acc)
    report("sunday", "saturday", acc)
    report("plasma", "altruism", acc)
    report("abcdef", "azced", acc)
    report("distance", "instance", acc)
    report("x", "", acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()

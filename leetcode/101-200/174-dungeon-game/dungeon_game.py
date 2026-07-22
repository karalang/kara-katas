"""LeetCode 174 — Dungeon Game (Python mirror / oracle).

Backward 2D DP: dp[i][j] = min health needed on entering (i,j) to survive =
max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]), filled from bottom-right.
Mirrors the Kāra version.
"""


def calculate_minimum_hp(dungeon):
    m = len(dungeon)
    n = len(dungeon[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                need = max(1, 1 - dungeon[i][j])
            elif i == m - 1:
                need = max(1, dp[i][j + 1] - dungeon[i][j])
            elif j == n - 1:
                need = max(1, dp[i + 1][j] - dungeon[i][j])
            else:
                ahead = min(dp[i + 1][j], dp[i][j + 1])
                need = max(1, ahead - dungeon[i][j])
            dp[i][j] = need
    return dp[0][0]


def report(dungeon):
    print(calculate_minimum_hp(dungeon))


def main():
    report([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]])
    report([[0]])
    report([[100]])
    report([[-3]])
    report([[1, -3, 3], [0, -2, 0], [-3, -3, -3]])
    report([[-200]])


main()

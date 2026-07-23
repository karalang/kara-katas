"""Benchmark workload for LeetCode #174 — Dungeon Game (Python; scale lane)."""


def calculate_minimum_hp(grid, dp, m, n):
    for i in range(m - 1, -1, -1):
        base = i * n
        for j in range(n - 1, -1, -1):
            cell = grid[base + j]
            if i == m - 1 and j == n - 1:
                need = max(1, 1 - cell)
            elif i == m - 1:
                need = max(1, dp[base + j + 1] - cell)
            elif j == n - 1:
                need = max(1, dp[base + n + j] - cell)
            else:
                ahead = min(dp[base + n + j], dp[base + j + 1])
                need = max(1, ahead - cell)
            dp[base + j] = need
    return dp[0]


def main():
    m, n, passes = 200, 200, 2000
    total = m * n
    grid = [0] * total
    state = 12345
    for c in range(total):
        state = (state * 1103515245 + 12345) & 2147483647
        grid[c] = (state % 121) - 100
    dp = [0] * total
    sink = 0
    for p in range(passes):
        idx = (p * 131 + 7) % total
        grid[idx] = -grid[idx]
        sink += calculate_minimum_hp(grid, dp, m, n)
    print(sink)


main()

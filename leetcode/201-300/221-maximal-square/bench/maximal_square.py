"""Benchmark workload for LeetCode #221 — Maximal Square (Python; scale lane)."""


def max_side(grid, dp, rows, cols):
    for j in range(cols):
        dp[j] = 0
    best = 0
    for i in range(rows):
        base = i * cols
        prev_diag = 0
        for j in range(cols):
            temp = dp[j]
            if grid[base + j] == 1:
                if i != 0 and j != 0:
                    m = dp[j]
                    if dp[j - 1] < m:
                        m = dp[j - 1]
                    if prev_diag < m:
                        m = prev_diag
                    v = m + 1
                else:
                    v = 1
                dp[j] = v
                if v > best:
                    best = v
            else:
                dp[j] = 0
            prev_diag = temp
    return best


def main():
    rows = 800
    cols = 800
    passes = 150
    total = rows * cols
    grid = [0] * total
    state = 12345
    for c in range(total):
        state = (state * 1103515245 + 12345) & 2147483647
        grid[c] = 1 if state % 100 < 62 else 0
    dp = [0] * cols
    sink = 0
    for p in range(passes):
        idx = (p % rows) * cols + ((p * 131 + 7) % cols)
        grid[idx] = 1 - grid[idx]
        sink += max_side(grid, dp, rows, cols)
    print(sink)


main()

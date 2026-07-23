#include <stdio.h>
#include <stdlib.h>

static long max_i64(long a, long b) { return a > b ? a : b; }
static long min_i64(long a, long b) { return a < b ? a : b; }

static long calculate_minimum_hp(const long *grid, long *dp, long m, long n) {
    for (long i = m - 1; i >= 0; i--) {
        long base = i * n;
        for (long j = n - 1; j >= 0; j--) {
            long cell = grid[base + j];
            long need = 0;
            if (i == m - 1 && j == n - 1) {
                need = max_i64(1, 1 - cell);
            } else if (i == m - 1) {
                need = max_i64(1, dp[base + j + 1] - cell);
            } else if (j == n - 1) {
                need = max_i64(1, dp[base + n + j] - cell);
            } else {
                long ahead = min_i64(dp[base + n + j], dp[base + j + 1]);
                need = max_i64(1, ahead - cell);
            }
            dp[base + j] = need;
        }
    }
    return dp[0];
}

int main(void) {
    long m = 200, n = 200, passes = 2000;
    long total = m * n;
    long *grid = malloc(total * sizeof(long));
    long state = 12345;
    for (long c = 0; c < total; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        grid[c] = (state % 121) - 100;
    }
    long *dp = calloc(total, sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 131 + 7) % total;
        grid[idx] = -grid[idx];
        sink += calculate_minimum_hp(grid, dp, m, n);
    }
    printf("%ld\n", sink);
    free(grid); free(dp);
    return 0;
}

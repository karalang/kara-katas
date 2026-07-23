#include <stdio.h>
#include <stdlib.h>

static long max_side(const long *grid, long *dp, long rows, long cols) {
    for (long j = 0; j < cols; j++) dp[j] = 0;
    long best = 0;
    for (long i = 0; i < rows; i++) {
        long base = i * cols;
        long prev_diag = 0;
        for (long j = 0; j < cols; j++) {
            long temp = dp[j];
            if (grid[base + j] == 1) {
                long v = 1;
                if (i != 0 && j != 0) {
                    long m = dp[j];
                    if (dp[j-1] < m) m = dp[j-1];
                    if (prev_diag < m) m = prev_diag;
                    v = m + 1;
                }
                dp[j] = v;
                if (v > best) best = v;
            } else {
                dp[j] = 0;
            }
            prev_diag = temp;
        }
    }
    return best;
}

int main(void) {
    long rows = 800, cols = 800, passes = 150;
    long total = rows * cols;
    long *grid = malloc(total * sizeof(long));
    long state = 12345;
    for (long c = 0; c < total; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        grid[c] = (state % 100 < 62) ? 1 : 0;
    }
    long *dp = calloc(cols, sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p % rows) * cols + ((p * 131 + 7) % cols);
        grid[idx] = 1 - grid[idx];
        sink += max_side(grid, dp, rows, cols);
    }
    printf("%ld\n", sink);
    free(grid); free(dp);
    return 0;
}

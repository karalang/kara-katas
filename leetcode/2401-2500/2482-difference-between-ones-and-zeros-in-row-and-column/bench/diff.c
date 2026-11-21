// LeetCode #2482: Difference Between Ones and Zeros in Row and Column --
// bench, C mirror of diff.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// the answer for an `m` by `n` grid, written into a fresh `m * n` array
static int64_t *ones_minus_zeros(int64_t *grid, int64_t m, int64_t n) {
    int64_t *row_ones = calloc((size_t)m, sizeof(int64_t));
    int64_t *col_ones = calloc((size_t)n, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++)
        for (int64_t j = 0; j < n; j++) {
            row_ones[i] += grid[i * n + j];
            col_ones[j] += grid[i * n + j];
        }
    int64_t *diff = malloc((size_t)(m * n) * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++)
        for (int64_t j = 0; j < n; j++) diff[i * n + j] = 2 * row_ones[i] + 2 * col_ones[j] - m - n;
    free(row_ones);
    free(col_ones);
    return diff;
}

static int64_t seed = 2482;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t grids[20][100 * 100];
    for (int g = 0; g < 20; g++)
        for (int c = 0; c < 100 * 100; c++) grids[g][c] = next_random() % 2;
    int64_t check = 0;
    for (int64_t p = 0; p < 180; p++) {
        for (int g = 0; g < 20; g++) {
            int64_t i = check % 100, j = check / 100 % 100;
            grids[g][i * 100 + j] = 1 - grids[g][i * 100 + j];
            int64_t *diff = ones_minus_zeros(grids[g], 100, 100);
            for (int c = 0; c < 100 * 100; c++) check = (check * 31 + diff[c] + 200 + p) % 1000000007;
            free(diff);
        }
    }
    printf("180 passes over 20 grids of 100 by 100: checksum %lld\n", (long long)check);
    return 0;
}

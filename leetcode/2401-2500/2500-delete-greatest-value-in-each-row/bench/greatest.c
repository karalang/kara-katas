// LeetCode #2500: Delete Greatest Value in Each Row -- C mirror of the
// benchmark (greatest.kara): the same grids, passes and checksum; each ask
// copies the grid and sorts every row with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2500;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t grids[1000][50][50];

static int ascending(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t delete_greatest_value(int64_t (*grid)[50]) {
    int64_t rows[50][50];
    memcpy(rows, grid, sizeof rows);
    for (int r = 0; r < 50; r++) qsort(rows[r], 50, sizeof(int64_t), ascending);
    int64_t total = 0;
    for (int j = 0; j < 50; j++) {
        int64_t most = 0;
        for (int r = 0; r < 50; r++) {
            if (rows[r][j] > most) most = rows[r][j];
        }
        total += most;
    }
    return total;
}

int main(void) {
    const int64_t passes = 32;
    for (int g = 0; g < 1000; g++)
        for (int r = 0; r < 50; r++)
            for (int c = 0; c < 50; c++) grids[g][r][c] = next_random() % 100 + 1;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int g = 0; g < 1000; g++) {
            int64_t r = check % 50, c = check / 50 % 50;
            int64_t was = grids[g][r][c];
            grids[g][r][c] = (check + p) % 100 + 1;
            check = (check * 31 + delete_greatest_value(grids[g]) + p) % 1000000007;
            grids[g][r][c] = was;
        }
    }
    printf("%lld passes over 1000 grids of 50 by 50: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}

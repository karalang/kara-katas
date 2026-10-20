// LeetCode 807 — Max Increase to Keep City Skyline: the bench.
//
// 64 grids of 50 by 50, LeetCode's largest, with heights from 0 to 100,
// are made once; each round finds how much the next one can grow.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t max_increase_keeping_skyline(int64_t **grid, int n) {
    int64_t *row_max = calloc(n, sizeof(int64_t));
    int64_t *col_max = calloc(n, sizeof(int64_t));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (grid[i][j] > row_max[i]) row_max[i] = grid[i][j];
            if (grid[i][j] > col_max[j]) col_max[j] = grid[i][j];
        }
    }
    int64_t total = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int64_t cap = row_max[i] < col_max[j] ? row_max[i] : col_max[j];
            total += cap - grid[i][j];
        }
    }
    free(row_max);
    free(col_max);
    return total;
}

int main(void) {
    int64_t seed = 807;
    int64_t **grids[64];
    for (int g = 0; g < 64; g++) {
        grids[g] = malloc(50 * sizeof(int64_t *));
        for (int i = 0; i < 50; i++) {
            grids[g][i] = malloc(50 * sizeof(int64_t));
            for (int j = 0; j < 50; j++) grids[g][i][j] = next_random(&seed) % 101;
        }
    }
    int64_t rounds = 300000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t added = max_increase_keeping_skyline(grids[r % 64], 50);
        total += added;
        check = (check * 131 + added) % 1000000007;
    }
    printf("%lld rounds of 50 x 50: %lld floors in all, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)check);
    return 0;
}

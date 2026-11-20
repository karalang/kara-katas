// LeetCode #1267 bench, in C: the ★ arm (the servers in each row and each
// column counted, then each server that shares its row or column with
// another counted) on 100 random 100-by-100 grids built once, a cell a
// server one time in 2 to 9, 300 rounds; every answer folded into a
// checksum. Each row is its own array, as LeetCode's `int[][]` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_servers(int64_t **grid, int m, int n) {
    int64_t *rows = calloc(m, sizeof(int64_t));
    int64_t *cols = calloc(n, sizeof(int64_t));
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (grid[r][c] == 1) {
                rows[r]++;
                cols[c]++;
            }
    int64_t count = 0;
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++)
            if (grid[r][c] == 1 && (rows[r] > 1 || cols[c] > 1)) count++;
    free(rows);
    free(cols);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1267;
    int64_t **grids[100];
    for (int g = 0; g < 100; g++) {
        int64_t odds = next_random(&seed) % 8 + 2;
        grids[g] = malloc(100 * sizeof(int64_t *));
        for (int r = 0; r < 100; r++) {
            grids[g][r] = malloc(100 * sizeof(int64_t));
            for (int c = 0; c < 100; c++) grids[g][r][c] = next_random(&seed) % odds == 0 ? 1 : 0;
        }
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 300; round++)
        for (int g = 0; g < 100; g++)
            check = (check * 131 + count_servers(grids[g], 100, 100) + round) % 1000000007;
    printf("300 rounds of 100 grids of 100 by 100: checksum %lld\n", (long long)check);
    return 0;
}

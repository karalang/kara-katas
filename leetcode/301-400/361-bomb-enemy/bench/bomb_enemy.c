// Benchmark for #361 -- mirror of bomb_enemy.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 400

static int64_t max_killed_enemies(char grid[N][N], int rows, int cols) {
    int64_t best = 0, row_hits = 0;
    int64_t col_hits[N] = {0};
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (j == 0 || grid[i][j - 1] == 'W') {
                row_hits = 0;
                for (int k = j; k < cols && grid[i][k] != 'W'; k++)
                    if (grid[i][k] == 'E') row_hits++;
            }
            if (i == 0 || grid[i - 1][j] == 'W') {
                col_hits[j] = 0;
                for (int k = i; k < rows && grid[k][j] != 'W'; k++)
                    if (grid[k][j] == 'E') col_hits[j]++;
            }
            if (grid[i][j] == '0' && row_hits + col_hits[j] > best) best = row_hits + col_hits[j];
        }
    }
    return best;
}

int main(void) {
    int64_t seed = 361, total = 0, checksum = 0;
    char (*grid)[N] = malloc(N * N);
    for (int g = 0; g < 60; g++) {
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                int64_t r = (seed / 65536) % 6;
                grid[i][j] = r == 0 ? 'W' : r < 3 ? 'E' : '0';
            }
        int64_t best = max_killed_enemies(grid, N, N);
        total += best;
        checksum = (checksum * 31 + best) % 1000000007;
    }
    printf("60 grids: %lld enemies in total, checksum %lld\n", (long long)total, (long long)checksum);
    free(grid);
    return 0;
}

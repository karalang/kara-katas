// LeetCode #2428: Maximum Sum of an Hourglass -- the bench, the ★ arm:
// every centre off the border, its seven cells added directly. Each grid
// is an array of row pointers, as the other languages' lists of rows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 150

static int64_t max_sum(int64_t **grid, int m, int n) {
    int64_t best = 0;
    for (int r = 1; r < m - 1; r++)
        for (int c = 1; c < n - 1; c++) {
            int64_t sum = grid[r - 1][c - 1] + grid[r - 1][c] + grid[r - 1][c + 1]
                + grid[r][c]
                + grid[r + 1][c - 1] + grid[r + 1][c] + grid[r + 1][c + 1];
            if (sum > best) best = sum;
        }
    return best;
}

static int64_t seed = 2428;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t **grids[10];
    for (int g = 0; g < 10; g++) {
        grids[g] = malloc(N * sizeof(int64_t *));
        for (int r = 0; r < N; r++) {
            grids[g][r] = malloc(N * sizeof(int64_t));
            for (int c = 0; c < N; c++) {
                int64_t a = next_random();
                grids[g][r][c] = (a * 32768 + next_random()) % 1000001;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 600; p++)
        for (int g = 0; g < 10; g++) {
            grids[g][(p * 37) % N][(p * 91) % N] = (p * 7919) % 1000001;
            check = (check * 31 + max_sum(grids[g], N, N) + p) % 1000000007;
        }
    printf("600 passes over 10 grids of 150 by 150: checksum %lld\n", (long long)check);
    for (int g = 0; g < 10; g++) {
        for (int r = 0; r < N; r++) free(grids[g][r]);
        free(grids[g]);
    }
    return 0;
}

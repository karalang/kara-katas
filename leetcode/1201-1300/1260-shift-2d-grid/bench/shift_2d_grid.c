// LeetCode #1260 bench, in C: the ★ arm (each value at flat place p
// written to (p + k) % (m * n) of a new grid) on 200 random grids of 50 by
// 50 built once, each shifted by a random 0 to 100, 150 rounds; a corner and
// the middle of each result folded into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// A grid as rows of `n` values, each row its own allocation, as the other
// languages' nested lists are.
static int64_t **shift_grid(int64_t **grid, int64_t m, int64_t n, int64_t k) {
    int64_t total = m * n;
    int64_t **shifted = malloc(m * sizeof(int64_t *));
    for (int64_t i = 0; i < m; i++) shifted[i] = calloc(n, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++)
        for (int64_t j = 0; j < n; j++) {
            int64_t to = (i * n + j + k) % total;
            shifted[to / n][to % n] = grid[i][j];
        }
    return shifted;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1260;
    int64_t **grids[200];
    int64_t shifts[200];
    for (int g = 0; g < 200; g++) {
        grids[g] = malloc(50 * sizeof(int64_t *));
        for (int i = 0; i < 50; i++) {
            grids[g][i] = malloc(50 * sizeof(int64_t));
            for (int j = 0; j < 50; j++) grids[g][i][j] = next_random(&seed) % 2001 - 1000;
        }
        shifts[g] = next_random(&seed) % 101;
    }
    int64_t check = 0;
    for (int r = 0; r < 150; r++)
        for (int g = 0; g < 200; g++) {
            int64_t **s = shift_grid(grids[g], 50, 50, shifts[g]);
            check = (check * 131 + s[0][0] + 1000) % 1000000007;
            check = (check * 131 + s[25][25] + 1000) % 1000000007;
            for (int i = 0; i < 50; i++) free(s[i]);
            free(s);
        }
    printf("150 rounds of 200 grids of 50 by 50: checksum %lld\n", (long long)check);
    return 0;
}

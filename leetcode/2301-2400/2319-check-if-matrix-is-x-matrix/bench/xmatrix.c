// LeetCode #2319: Check if Matrix Is X-Matrix -- the bench, the ★ arm in
// C. One walk over the cells, a cell on either diagonal nonzero and any
// other zero, the first cell that breaks its rule ending the walk.
// O(n^2). Each grid is an array of row pointers, as the others' are a
// list of rows.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool check_x_matrix(int64_t **grid, int64_t n) {
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < n; j++) {
            bool on = i == j || i + j == n - 1;
            if (on != (grid[i][j] != 0))
                return false;
        }
    return true;
}

static int64_t seed = 2319;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100;
    int64_t **grids[200];
    for (int g = 0; g < 200; g++) {
        grids[g] = malloc(n * sizeof(int64_t *));
        for (int64_t i = 0; i < n; i++) {
            grids[g][i] = malloc(n * sizeof(int64_t));
            for (int64_t j = 0; j < n; j++) {
                int64_t value = next_random() % 100000 + 1;
                grids[g][i][j] = (i == j || i + j == n - 1) ? value : 0;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 400; p++)
        for (int g = 0; g < 200; g++) {
            bool punch = next_random() % 2 == 0;
            int64_t i = next_random() % n;
            int64_t j = next_random() % n;
            int64_t old = grids[g][i][j];
            if (punch)
                grids[g][i][j] = old == 0 ? p + 1 : 0;
            bool is_x = check_x_matrix(grids[g], n);
            grids[g][i][j] = old;
            check = (check * 31 + (is_x ? 2 : 1) + p) % 1000000007;
        }
    printf("400 passes over 200 grids of 100 by 100: checksum %lld\n", (long long)check);
    for (int g = 0; g < 200; g++) {
        for (int64_t i = 0; i < n; i++)
            free(grids[g][i]);
        free(grids[g]);
    }
    return 0;
}

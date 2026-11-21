// LeetCode #2435: Paths in Matrix Whose Sum Is Divisible by K -- the
// bench, the ★ arm: one row of counts by remainder, each cell's from
// above, still in place, and from the left, shifted by its value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t number_of_paths(int64_t **grid, int64_t m, int64_t n, int64_t k) {
    int64_t **row = malloc(n * sizeof(int64_t *));
    for (int64_t j = 0; j < n; j++) row[j] = calloc(k, sizeof(int64_t));
    int64_t *came = malloc(k * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++)
        for (int64_t j = 0; j < n; j++) {
            for (int64_t r = 0; r < k; r++) came[r] = 0;
            if (i == 0 && j == 0) came[0] = 1;
            for (int64_t r = 0; r < k; r++) {
                int64_t left = j > 0 ? row[j - 1][r] : 0;
                came[r] = (came[r] + row[j][r] + left) % MOD;
            }
            int64_t v = grid[i][j];
            for (int64_t r = 0; r < k; r++) row[j][(r + v) % k] = came[r];
        }
    int64_t answer = row[n - 1][0];
    for (int64_t j = 0; j < n; j++) free(row[j]);
    free(row);
    free(came);
    return answer;
}

static int64_t seed = 2435;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 5, m = 200, n = 250;
    int64_t ***grids = malloc(count * sizeof(int64_t **));
    for (int64_t g = 0; g < count; g++) {
        grids[g] = malloc(m * sizeof(int64_t *));
        for (int64_t i = 0; i < m; i++) {
            grids[g][i] = malloc(n * sizeof(int64_t));
            for (int64_t j = 0; j < n; j++) grids[g][i][j] = next_random() % 101;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int64_t g = 0; g < count; g++) {
            grids[g][(p * 37) % m][(p * 91) % n] = p;
            check = (check * 31 + number_of_paths(grids[g], m, n, 50) + p) % 1000000007;
        }
    printf("10 passes over 5 grids of 200 by 250: checksum %lld\n", (long long)check);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < m; i++) free(grids[g][i]);
        free(grids[g]);
    }
    free(grids);
    return 0;
}

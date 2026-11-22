// LeetCode #2732: Find a Good Subset of the Matrix -- the bench
// (subset.kara in C): a row of zeros alone, or the first rows of two
// disjoint masks among the 32. Each grid is one flat array of m * n
// cells; the answer goes into out[], its length returned.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int good_subsetof_binary_matrix(const int64_t *grid, int64_t m, int64_t n, int64_t *out) {
    int64_t first[32];
    for (int k = 0; k < 32; k++) first[k] = -1;
    for (int64_t i = 0; i < m; i++) {
        int64_t mask = 0;
        for (int64_t j = 0; j < n; j++) mask |= grid[i * n + j] << j;
        if (mask == 0) {
            out[0] = i;
            return 1;
        }
        if (first[mask] < 0) first[mask] = i;
    }
    for (int a = 1; a < 32; a++) {
        for (int b = a + 1; b < 32; b++) {
            if ((a & b) == 0 && first[a] >= 0 && first[b] >= 0) {
                out[0] = first[a] < first[b] ? first[a] : first[b];
                out[1] = first[a] < first[b] ? first[b] : first[a];
                return 2;
            }
        }
    }
    return 0;
}

static int64_t seed = 2732;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int grids = 100, rounds = 10;
    const int64_t m = 10000, n = 5;
    int64_t *all = malloc(sizeof(int64_t) * grids * m * n);
    for (int g = 0; g < grids; g++) {
        int kind = g % 3;
        int64_t column = next_random() % n;
        int64_t free_row = next_random() % m;
        int64_t *grid = all + (int64_t)g * m * n;
        for (int64_t r = 0; r < m; r++) {
            for (int64_t j = 0; j < n; j++) grid[r * n + j] = next_random() % 2;
            if (kind == 1 || (kind == 2 && r != free_row)) grid[r * n + column] = 1;
        }
    }
    int64_t found = 0, check = 0, out[2];
    for (int r = 0; r < rounds; r++) {
        for (int g = 0; g < grids; g++) {
            int len = good_subsetof_binary_matrix(all + (int64_t)g * m * n, m, n, out);
            if (len > 0) found++;
            int64_t named = 0;
            for (int k = 0; k < len; k++) named += out[k];
            check = (check * 31 + named + len + r) % 1000000007;
        }
    }
    printf("%d grids of %lld rows, %d rounds: %lld good subsets found, checksum %lld\n", grids, (long long)m, rounds, (long long)found, (long long)check);
    free(all);
    return 0;
}

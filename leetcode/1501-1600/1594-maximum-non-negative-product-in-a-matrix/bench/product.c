// LeetCode #1594: Maximum Non Negative Product in a Matrix
// -- the bench in C, mirroring product.kara: the largest and the smallest
// product of a path reaching each cell, in two malloc'd tables of rows,
// on 40000 grids of 15 by 15 cells from -4 to 4, all drawn first; each
// grid is a malloc'd array of malloc'd rows, as Kāra's Vec[Vec[i32]] is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 1594;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int32_t max_product_path(int32_t **grid, int rows, int cols) {
    int64_t **hi = malloc(sizeof(int64_t *) * rows);
    int64_t **lo = malloc(sizeof(int64_t *) * rows);
    for (int r = 0; r < rows; r++) {
        hi[r] = calloc(cols, sizeof(int64_t));
        lo[r] = calloc(cols, sizeof(int64_t));
    }
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            int64_t v = grid[r][c];
            if (r == 0 && c == 0) {
                hi[r][c] = v;
                lo[r][c] = v;
                continue;
            }
            int64_t best = INT64_MIN, worst = INT64_MAX, x;
            if (r > 0) {
                x = hi[r - 1][c] * v; if (x > best) best = x; if (x < worst) worst = x;
                x = lo[r - 1][c] * v; if (x > best) best = x; if (x < worst) worst = x;
            }
            if (c > 0) {
                x = hi[r][c - 1] * v; if (x > best) best = x; if (x < worst) worst = x;
                x = lo[r][c - 1] * v; if (x > best) best = x; if (x < worst) worst = x;
            }
            hi[r][c] = best;
            lo[r][c] = worst;
        }
    }
    int64_t top = hi[rows - 1][cols - 1];
    for (int r = 0; r < rows; r++) {
        free(hi[r]);
        free(lo[r]);
    }
    free(hi);
    free(lo);
    return top < 0 ? -1 : (int32_t)(top % 1000000007);
}

int main(void) {
    enum { N = 40000, S = 15 };
    int32_t ***grids = malloc(sizeof(int32_t **) * N);
    for (int g = 0; g < N; g++) {
        grids[g] = malloc(sizeof(int32_t *) * S);
        for (int r = 0; r < S; r++) {
            grids[g][r] = malloc(sizeof(int32_t) * S);
            for (int c = 0; c < S; c++) grids[g][r][c] = (int32_t)(next_random() % 9 - 4);
        }
    }
    int64_t check = 0;
    int negative = 0;
    for (int g = 0; g < N; g++) {
        int32_t answer = max_product_path(grids[g], S, S);
        if (answer == -1) negative++;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("40000 grids of 15 by 15: %d only negative, checksum %lld\n", negative, (long long)check);
    for (int g = 0; g < N; g++) {
        for (int r = 0; r < S; r++) free(grids[g][r]);
        free(grids[g]);
    }
    free(grids);
    return 0;
}

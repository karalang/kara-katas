// LeetCode #1314 bench, C: the ★ arm (a table of sums over every top-left
// rectangle, each block's sum four lookups) on the same 20 matrices and 200
// passes. Each call takes a fresh table and answer, as the others do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

static int64_t imax(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t imin(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t *matrix_block_sum(const int64_t *mat, int64_t m, int64_t n, int64_t k) {
    int64_t w = n + 1;
    int64_t *sums = calloc((size_t)((m + 1) * w), sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        for (int64_t j = 0; j < n; j++) {
            sums[(i + 1) * w + j + 1] = mat[i * n + j] + sums[i * w + j + 1] + sums[(i + 1) * w + j] - sums[i * w + j];
        }
    }
    int64_t *out = malloc(sizeof(int64_t) * (size_t)(m * n));
    for (int64_t i = 0; i < m; i++) {
        int64_t top = imax(i - k, 0), bottom = imin(i + k + 1, m);
        for (int64_t j = 0; j < n; j++) {
            int64_t left = imax(j - k, 0), right = imin(j + k + 1, n);
            out[i * n + j] = sums[bottom * w + right] - sums[top * w + right] - sums[bottom * w + left] + sums[top * w + left];
        }
    }
    free(sums);
    return out;
}

static int64_t seed = 1314;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t mats[20][N * N];
    for (int g = 0; g < 20; g++) {
        for (int c = 0; c < N * N; c++) mats[g][c] = 1 + next_random() % 100;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 200; pass++) {
        for (int g = 0; g < 20; g++) {
            mats[g][(check % N) * N + (check / 7) % N] = 1 + (check / 11) % 100;
            int64_t k = check % 4 == 0 ? 1 + (check / 13) % 100 : 1 + (check / 13) % 5;
            int64_t *got = matrix_block_sum(mats[g], N, N, k);
            check = (check * 31 + got[((check / 3) % N) * N + (check / 17) % N]) % 1000000007;
            check = (check * 31 + got[((check / 19) % N) * N + (check / 23) % N] + pass) % 1000000007;
            free(got);
        }
    }
    printf("200 passes over 20 matrices of 100 by 100: checksum %lld\n", (long long)check);
    return 0;
}

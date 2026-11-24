// LeetCode #1329 bench, C mirror of the Kāra bench: the ★ arm (each
// diagonal read into a buffer, sorted with `qsort` and written back) on 8
// matrices of 300 by 300, values 1 to 100, built once. Then 100 passes,
// each setting one cell of every matrix from the checksum so far,
// answering it and folding two of the answer's cells plus the pass into
// the checksum. Each call copies the matrix row by row into fresh rows and
// takes a fresh buffer for each diagonal, as the Kāra arm clones its
// `Vec[Vec[i32]]` and takes a fresh `Vec` per diagonal.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 300

static int cmp_i32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static void sort_from(int32_t **out, int64_t m, int64_t n, int64_t i0, int64_t j0) {
    int64_t len = 0;
    while (i0 + len < m && j0 + len < n) len++;
    int32_t *vals = malloc((size_t)len * sizeof(int32_t));
    for (int64_t k = 0; k < len; k++) vals[k] = out[i0 + k][j0 + k];
    qsort(vals, (size_t)len, sizeof(int32_t), cmp_i32);
    for (int64_t k = 0; k < len; k++) out[i0 + k][j0 + k] = vals[k];
    free(vals);
}

static int32_t **diagonal_sort(int32_t **mat, int64_t m, int64_t n) {
    int32_t **out = malloc((size_t)m * sizeof(int32_t *));
    for (int64_t i = 0; i < m; i++) {
        out[i] = malloc((size_t)n * sizeof(int32_t));
        memcpy(out[i], mat[i], (size_t)n * sizeof(int32_t));
    }
    for (int64_t i = 0; i < m; i++) sort_from(out, m, n, i, 0);
    for (int64_t j = 1; j < n; j++) sort_from(out, m, n, 0, j);
    return out;
}

static int64_t seed = 1329;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t **mats[8];
    for (int t = 0; t < 8; t++) {
        mats[t] = malloc(SIZE * sizeof(int32_t *));
        for (int i = 0; i < SIZE; i++) {
            mats[t][i] = malloc(SIZE * sizeof(int32_t));
            for (int j = 0; j < SIZE; j++) mats[t][i][j] = (int32_t)(1 + next_random() % 100);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int t = 0; t < 8; t++) {
            int64_t r = check % SIZE;
            int64_t c = (check / 7) % SIZE;
            mats[t][r][c] = (int32_t)(1 + (check / 13) % 100);
            int32_t **out = diagonal_sort(mats[t], SIZE, SIZE);
            check = (check * 31 + out[r][c] + out[SIZE - 1][SIZE / 2] + pass) % 1000000007;
            for (int i = 0; i < SIZE; i++) free(out[i]);
            free(out);
        }
    }
    printf("100 passes over 8 matrices of 300 by 300: checksum %lld\n", (long long)check);
    return 0;
}

/*
 * Benchmark workload — Search a 2D Matrix (LeetCode #74).
 * C mirror of bench/search_a_2d_matrix.kara. Flattened binary search over a
 * 100x100 matrix built ONCE as int64_t** (row pointers into per-row mallocs —
 * double-indirection, matching Kara's Vec[Vec[i64]] indexing, NOT a flat 1-D
 * array), then K=10,000,000 queries (targets k % 20000, ~half hit) folding each
 * hit/miss bit into a rolling polynomial hash. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int search_matrix(int64_t **m, int64_t rows, int64_t cols, int64_t target) {
    if (rows == 0) return 0;
    if (cols == 0) return 0;
    int64_t lo = 0, hi = rows * cols - 1;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t v = m[mid / cols][mid % cols];
        if (v == target) return 1;
        else if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}

int main(void) {
    const int64_t rows = 100, cols = 100;
    const int64_t total = 10000000, modulus = 1000000007;
    const int64_t range = 2 * rows * cols;

    int64_t **m = (int64_t **)malloc(sizeof(int64_t *) * (size_t)rows);
    for (int64_t i = 0; i < rows; i++) {
        m[i] = (int64_t *)malloc(sizeof(int64_t) * (size_t)cols);
        for (int64_t j = 0; j < cols; j++)
            m[i][j] = (i * cols + j) * 2;
    }

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t target = k % range;
        int64_t bit = search_matrix(m, rows, cols, target) ? 1 : 0;
        acc = (acc * 131 + bit) % modulus;
    }
    printf("%lld\n", (long long)acc);

    for (int64_t i = 0; i < rows; i++) free(m[i]);
    free(m);
    return 0;
}

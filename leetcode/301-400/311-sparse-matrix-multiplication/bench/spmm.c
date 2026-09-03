/* Benchmark mirror — LeetCode 311, Sparse Matrix Multiplication.
 * Same flat row-major layout, same LCG, same zero-skipping multiply, same
 * per-pass perturbation and masked sink as spmm.kara. See ../README.md. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 320, passes = 620;
    int64_t *a = malloc((size_t)(n * n) * sizeof(int64_t));
    int64_t *b = malloc((size_t)(n * n) * sizeof(int64_t));
    int64_t *c = malloc((size_t)(n * n) * sizeof(int64_t));
    int64_t state = 20311;
    for (int64_t i = 0; i < n * n; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        if (state % 100 < 4) { state = (state * 1103515245 + 12345) % 2147483648; a[i] = state % 9 - 4; }
        else a[i] = 0;
        state = (state * 1103515245 + 12345) % 2147483648;
        if (state % 100 < 4) { state = (state * 1103515245 + 12345) % 2147483648; b[i] = state % 9 - 4; }
        else b[i] = 0;
    }

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t slot = (p * 7919) % (n * n);
        a[slot] = a[slot] + (checksum & 1);
        for (int64_t i = 0; i < n * n; i++) c[i] = 0;
        for (int64_t r = 0; r < n; r++) {
            int64_t arow = r * n;
            for (int64_t k = 0; k < n; k++) {
                int64_t av = a[arow + k];
                if (av != 0) {
                    int64_t brow = k * n;
                    for (int64_t j = 0; j < n; j++) c[arow + j] += av * b[brow + j];
                }
            }
        }
        int64_t acc = 0;
        for (int64_t t = 0; t < n * n; t++) acc = (acc + c[t]) & 0x3FFFFFFF;
        checksum = (checksum + acc) & 0x3FFFFFFF;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}

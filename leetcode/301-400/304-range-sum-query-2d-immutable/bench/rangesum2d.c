/* Benchmark mirror — LeetCode 304, Range Sum Query 2D (Immutable).
 * Same algorithm, same flat prefix layout, same LCG, same masked sink as
 * rangesum2d.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 256, stride = n + 1;
    const int64_t queries = 100000, passes = 1800;
    int64_t state = 20304;

    int64_t *m = malloc((size_t)(n * n) * sizeof(int64_t));
    for (int64_t i = 0; i < n * n; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        m[i] = state % 21 - 10;
    }

    int64_t table = (n + 1) * stride;
    int64_t *pre = calloc((size_t)table, sizeof(int64_t));
    for (int64_t r = 0; r < n; r++)
        for (int64_t c = 0; c < n; c++)
            pre[(r + 1) * stride + (c + 1)] = pre[r * stride + (c + 1)]
                                            + pre[(r + 1) * stride + c]
                                            - pre[r * stride + c]
                                            + m[r * n + c];

    int64_t *qr1 = malloc((size_t)queries * sizeof(int64_t));
    int64_t *qc1 = malloc((size_t)queries * sizeof(int64_t));
    int64_t *qr2 = malloc((size_t)queries * sizeof(int64_t));
    int64_t *qc2 = malloc((size_t)queries * sizeof(int64_t));
    for (int64_t q = 0; q < queries; q++) {
        state = (state * 1103515245 + 12345) % 2147483648; int64_t a = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t b = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t c = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t d = state % n;
        if (a <= b) { qr1[q] = a; qr2[q] = b; } else { qr1[q] = b; qr2[q] = a; }
        if (c <= d) { qc1[q] = c; qc2[q] = d; } else { qc1[q] = d; qc2[q] = c; }
    }

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t k = 0; k < queries; k++) {
            int64_t r1 = qr1[k], c1 = qc1[k], r2 = qr2[k], c2 = qc2[k];
            int64_t v = pre[(r2 + 1) * stride + (c2 + 1)]
                      - pre[r1 * stride + (c2 + 1)]
                      - pre[(r2 + 1) * stride + c1]
                      + pre[r1 * stride + c1];
            checksum = (checksum + v) & 0x3FFFFFFF;
        }
    }

    printf("checksum %lld\n", (long long)checksum);
    return 0;
}

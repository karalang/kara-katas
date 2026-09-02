/* Benchmark mirror — LeetCode 307, Range Sum Query (Mutable).
 * Same Fenwick tree, same LCG-generated operation script, same masked sink as
 * fenwick.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 65536, ops = 200000, passes = 110;
    int64_t *tree = calloc((size_t)(n + 1), sizeof(int64_t));
    int64_t *data = calloc((size_t)n, sizeof(int64_t));
    int64_t *kind = malloc((size_t)ops * sizeof(int64_t));
    int64_t *opa  = malloc((size_t)ops * sizeof(int64_t));
    int64_t *opb  = malloc((size_t)ops * sizeof(int64_t));

    int64_t state = 20307;
    for (int64_t k = 0; k < ops; k++) {
        state = (state * 1103515245 + 12345) % 2147483648; int64_t t = state % 2;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t x = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t y = state % n;
        kind[k] = t;
        if (t == 0) { opa[k] = x; opb[k] = y % 2001 - 1000; }
        else if (x <= y) { opa[k] = x; opb[k] = y; }
        else { opa[k] = y; opb[k] = x; }
    }

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t k = 0; k < ops; k++) {
            if (kind[k] == 0) {
                int64_t i = opa[k];
                int64_t delta = opb[k] - data[i];
                data[i] = opb[k];
                for (int64_t x = i + 1; x <= n; x += x & -x) tree[x] += delta;
            } else {
                int64_t total = 0;
                for (int64_t hi = opb[k] + 1; hi > 0; hi -= hi & -hi) total += tree[hi];
                for (int64_t lo = opa[k];     lo > 0; lo -= lo & -lo) total -= tree[lo];
                checksum = (checksum + total) & 0x3FFFFFFF;
            }
        }
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}

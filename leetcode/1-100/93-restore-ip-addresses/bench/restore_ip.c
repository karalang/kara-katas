/*
 * Benchmark workload — Restore IP Addresses (LeetCode #93).
 * C mirror of bench/restore_ip.kara. Folds the segment values of every valid
 * four-segment quadruple through a rolling polynomial hash; digits computed inline from
 * the iteration index (no array). Input length varies per iteration (n = 4 + iter%9) so
 * the fixed-shape enumeration can't be vectorized away. K=6,500,000. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t digit(int64_t pos, int64_t iter) {
    return (pos * 7 + iter) % 10;
}

static int64_t seg_val(int64_t start, int64_t len, int64_t iter) {
    if (len < 1 || len > 3) return -1;
    if (len > 1 && digit(start, iter) == 0) return -1;
    int64_t v = 0;
    for (int64_t i = 0; i < len; i++)
        v = v * 10 + digit(start + i, iter);
    if (v > 255) return -1;
    return v;
}

static int64_t restore_fold(int64_t n, int64_t iter, int64_t seed) {
    int64_t acc = seed;
    for (int64_t a = 1; a <= 3 && a < n; a++) {
        int64_t v0 = seg_val(0, a, iter);
        if (v0 < 0) continue;
        for (int64_t b = a + 1; b <= a + 3 && b < n; b++) {
            int64_t v1 = seg_val(a, b - a, iter);
            if (v1 < 0) continue;
            for (int64_t c = b + 1; c <= b + 3 && c < n; c++) {
                int64_t v2 = seg_val(b, c - b, iter);
                int64_t v3 = seg_val(c, n - c, iter);
                if (v2 >= 0 && v3 >= 0)
                    acc = (acc * 131 + v0 * 1000000 + v1 * 10000 + v2 * 100 + v3 + 1) % 1000000007;
            }
        }
    }
    return acc;
}

int main(void) {
    const int64_t total = 6500000, modulus = 1000000007;
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t n = 4 + (iter % 9);            /* 4..12 — data-dependent length */
        sum = (sum * 131 + restore_fold(n, iter, iter)) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}

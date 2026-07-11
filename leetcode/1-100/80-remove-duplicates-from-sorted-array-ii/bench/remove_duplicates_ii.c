/*
 * Benchmark workload — Remove Duplicates from Sorted Array II (LeetCode #80).
 * C mirror of bench/remove_duplicates_ii.kara. The generalized run-scan computes the
 * at-most-2 dedup and folds each kept value through a rolling polynomial hash — the
 * loop-carried hash serialises the scan, and a fixed heap array built once avoids
 * per-iteration allocation. N=3000 sorted array with mixed run lengths, scanned
 * K=67000 times, seeded by the iteration index. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

/* 1D heap array (malloc'd int64_t*) — the same layout kara's Vec[i64] uses. */
static int64_t *build(int64_t n) {
    int64_t *arr = malloc(n * sizeof(int64_t));
    int64_t val = 0, pos = 0;
    while (pos < n) {
        int64_t runlen = (val % 3) + 1;
        for (int64_t r = 0; r < runlen && pos < n; r++)
            arr[pos++] = val;
        val++;
    }
    return arr;
}

static int64_t scan_fold(const int64_t *arr, int64_t n, int64_t seed) {
    int64_t acc = seed;
    int64_t i = 0;
    while (i < n) {
        int64_t v = arr[i];
        int64_t run = 0;
        while (i < n && arr[i] == v) {
            if (run < 2)
                acc = (acc * 131 + (v + 1)) % 1000000007;
            run++;
            i++;
        }
    }
    return acc;
}

int main(void) {
    const int64_t n = 3000, total = 67000, modulus = 1000000007;
    int64_t *arr = build(n);
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t r = scan_fold(arr, n, iter);
        sum = (sum + r) % modulus;
    }
    printf("%lld\n", (long long)sum);
    free(arr);
    return 0;
}

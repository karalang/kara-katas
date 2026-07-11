/*
 * Benchmark workload — Sort Colors (LeetCode #75).
 * C mirror of bench/sort_colors.kara. Dutch National Flag one-pass sort over an
 * int64_t buffer malloc'd ONCE (n=500) and reused: each of K=200,000 iterations
 * refills it in place with a k-dependent {0,1,2} pattern, sorts in place, and
 * folds the result into a rolling polynomial hash. The measured work is the
 * sort's data-dependent branches and swaps, not allocation.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static void sort_colors(int64_t *a, int64_t n) {
    if (n == 0) return;
    int64_t low = 0, mid = 0, high = n - 1;
    while (mid <= high) {
        if (a[mid] == 0) {
            int64_t t = a[low]; a[low] = a[mid]; a[mid] = t;
            low++;
            mid++;
        } else if (a[mid] == 1) {
            mid++;
        } else {
            int64_t t = a[mid]; a[mid] = a[high]; a[high] = t;
            high--;
        }
    }
}

int main(void) {
    const int64_t n = 500, total = 200000, modulus = 1000000007;
    int64_t *a = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        for (int64_t j = 0; j < n; j++)
            a[j] = (j * 7 + k * 13) % 3;
        sort_colors(a, n);
        for (int64_t j = 0; j < n; j++)
            acc = (acc * 131 + a[j]) % modulus;
    }
    printf("%lld\n", (long long)acc);

    free(a);
    return 0;
}

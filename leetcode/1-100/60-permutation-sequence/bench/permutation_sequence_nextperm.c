/* Benchmark workload — Permutation Sequence (LeetCode #60), NEXT-PERM solver.
 * C mirror of bench/permutation_sequence_nextperm.kara. Same M=9 rotated (n,k)
 * cases, K=333, next_permutation iterated k-1 times (O(k·n)). The array is
 * malloc'd per iter (one allocation, matching Kāra's single per-iter Vec). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static const int64_t NTAB[9] = {9, 8, 9, 7, 8, 9, 6, 7, 9};
static const int64_t KTAB[9] = {362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000};
#define M 9
#define K_ITERS 333LL

static void next_permutation(int64_t *a, int64_t len) {
    int64_t i = len - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;
    if (i >= 0) {
        int64_t j = len - 1;
        while (a[j] <= a[i]) j--;
        int64_t tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
    }
    int64_t lo = i + 1, hi = len - 1;
    while (lo < hi) {
        int64_t t = a[lo];
        a[lo] = a[hi];
        a[hi] = t;
        lo++;
        hi--;
    }
}

static int64_t get_permutation_checksum(int64_t n, int64_t k) {
    int64_t *a = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) a[i] = i + 1;
    for (int64_t step = 0; step < k - 1; step++) next_permutation(a, n);
    int64_t s = 0;
    for (int64_t i = 0; i < n; i++) s += a[i] * (i + 1);
    free(a);
    return s;
}

int main(void) {
    int64_t total = 0;
    for (int64_t k = 0; k < K_ITERS; k++) {
        int64_t idx = k % M;
        total += get_permutation_checksum(NTAB[idx], KTAB[idx]);
    }
    printf("%lld\n", (long long)total);
    return 0;
}

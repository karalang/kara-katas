/* Benchmark workload — Permutation Sequence (LeetCode #60), FACTORIAL solver.
 * C mirror of bench/permutation_sequence.kara. Same M=9 rotated (n,k) cases,
 * K=500k, factorial-number-system generator, position-weighted checksum, sink.
 * fact / digits / result are each malloc'd per iter (3 allocations), matching
 * Kāra's three per-iter Vecs — apples-to-apples on allocation, not stack
 * buffers that would elide the heap traffic. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static const int64_t NTAB[9] = {9, 8, 9, 7, 8, 9, 6, 7, 9};
static const int64_t KTAB[9] = {362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000};
#define M 9
#define K_ITERS 500000LL

static int64_t get_permutation_checksum(int64_t n, int64_t k) {
    int64_t *fact = (int64_t *)malloc(sizeof(int64_t) * (size_t)(n + 1));
    fact[0] = 1;
    for (int64_t i = 1; i <= n; i++) fact[i] = fact[i - 1] * i;

    int64_t *digits = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) digits[i] = i + 1;
    int64_t dn = n;

    int64_t *result = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);
    int64_t kk = k - 1;
    for (int64_t pos = 0; pos < n; pos++) {
        int64_t block = fact[n - 1 - pos];
        int64_t idx = kk / block;
        kk %= block;
        result[pos] = digits[idx];
        for (int64_t j = idx; j < dn - 1; j++) digits[j] = digits[j + 1];
        dn--;
    }

    int64_t s = 0;
    for (int64_t i = 0; i < n; i++) s += result[i] * (i + 1);
    free(fact);
    free(digits);
    free(result);
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

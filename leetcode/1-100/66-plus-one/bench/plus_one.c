/*
 * Benchmark workload — Plus One (LeetCode #66).
 * C mirror of bench/plus_one.kara. A fixed-width (W=9) decimal digit buffer
 * driven as a base-10 counter: the ★'s reverse-scan carry applied in place K
 * times, folding a rotating digit into a rolling polynomial-hash sink. In place,
 * no per-iter allocation — measures the carry-scan codegen, not the allocator.
 * K < 10^9 so the counter never overflows 9 digits (the array-widening path does
 * not fire). See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    const int64_t total = 80000000;
    const int64_t modulus = 1000000007;
    const int W = 9;

    int64_t digits[9] = {0};

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int i = W - 1;
        while (i >= 0) {
            if (digits[i] < 9) {
                digits[i] = digits[i] + 1;
                break;                 /* carry absorbed */
            }
            digits[i] = 0;
            i = i - 1;
        }
        acc = (acc * 131 + digits[k % W]) % modulus;
    }

    printf("%lld\n", (long long)acc);
    return 0;
}

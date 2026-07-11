/*
 * Benchmark workload — Gray Code (LeetCode #89).
 * C mirror of bench/gray_code.kara. Folds each gray code i ^ (i >> 1) through a rolling
 * polynomial hash (loop-carried, iter-mixed so nothing hoists), N=65536 codes, K=2500
 * iterations. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 65536, total = 2500, modulus = 1000000007;
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t acc = iter;
        for (int64_t i = 0; i < n; i++) {
            int64_t g = i ^ (i >> 1);
            acc = (acc * 131 + (g ^ iter)) % modulus;
        }
        sum = (sum * 131 + acc) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}

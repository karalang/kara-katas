/*
 * Benchmark workload — Unique Paths II (LeetCode #63).
 * C mirror of bench/unique_paths_ii.kara. Plain malloc/free rolling-DP array —
 * the same per-call `Vec[i64]` alloc + fill + drop, sized to the real column
 * count n (obstacles break #62's axis symmetry, so no swap), without any RC/GC
 * overhead: the cleanest LLVM-backend floor.
 *
 * Same K/span sweep, the same `dp[c] += dp[c-1]` recurrence, the same inline
 * obstacle predicate ((i*7 + c*3 + k) % 13 == 0), and the same rolling
 * polynomial-hash sink. All counts stay inside int64_t (bounded by the
 * unobstructed 33×33 count C(64,32) ≈ 1.8e18). See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t unique_paths_with_obstacles(int64_t m, int64_t n, int64_t k) {
    int64_t cols = n;

    int64_t *dp = (int64_t *)malloc((size_t)cols * sizeof(int64_t));
    for (int64_t j = 0; j < cols; j++) dp[j] = 0;
    dp[0] = 1;

    for (int64_t i = 0; i < m; i++) {
        for (int64_t c = 0; c < cols; c++) {
            if ((i * 7 + c * 3 + k) % 13 == 0) {
                dp[c] = 0;
            } else if (c > 0) {
                dp[c] = dp[c] + dp[c - 1];
            }
        }
    }

    int64_t r = dp[cols - 1];
    free(dp);
    return r;
}

int main(void) {
    const int64_t total = 1000000;
    const int64_t modulus = 1000000007;
    const int64_t span = 32;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t m = 2 + (k % span);
        int64_t n = 2 + ((k / span) % span);
        int64_t ans = unique_paths_with_obstacles(m, n, k);
        acc = (acc * 131 + ans) % modulus;
    }
    printf("%lld\n", (long long)acc);
    return 0;
}

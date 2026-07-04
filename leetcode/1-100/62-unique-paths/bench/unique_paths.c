/*
 * Benchmark workload — Unique Paths (LeetCode #62).
 * C mirror of bench/unique_paths.kara. Plain malloc/free rolling-DP array —
 * mirrors Kāra's per-call `Vec[i64]` alloc + fill + drop, sized to the smaller
 * axis, without any RC/GC overhead: the cleanest LLVM-backend floor.
 *
 * Same K/span sweep, the same `dp[c] += dp[c-1]` recurrence, and the same
 * rolling polynomial-hash sink. All counts stay inside int64_t (33×33 is the
 * largest case, C(64,32) ≈ 1.8e18). See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t unique_paths(int64_t m, int64_t n) {
    int64_t rows = m, cols = n;
    if (cols > rows) { int64_t t = rows; rows = cols; cols = t; }

    int64_t *dp = (int64_t *)malloc((size_t)cols * sizeof(int64_t));
    for (int64_t j = 0; j < cols; j++) dp[j] = 1;

    for (int64_t i = 1; i < rows; i++)
        for (int64_t c = 1; c < cols; c++)
            dp[c] = dp[c] + dp[c - 1];

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
        int64_t ans = unique_paths(m, n);
        acc = (acc * 131 + ans) % modulus;
    }
    printf("%lld\n", (long long)acc);
    return 0;
}

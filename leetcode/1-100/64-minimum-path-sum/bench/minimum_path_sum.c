/*
 * Benchmark workload — Minimum Path Sum (LeetCode #64).
 * C mirror of bench/minimum_path_sum.kara. Plain malloc/free rolling-DP array —
 * the same per-call `Vec[i64]` alloc + fill + drop, sized to the real column
 * count n (like #63, costs break #62's axis symmetry, so no swap), without any
 * RC/GC overhead: the cleanest LLVM-backend floor.
 *
 * Same K/span sweep, the same `dp[c] = cost + min(dp[c], dp[c-1])` recurrence,
 * the same inline cost predicate ((i*7 + c*3 + k) % 13 + 1, in [1,13]), and the
 * same rolling polynomial-hash sink. The answer is tiny (≤ ~300), far inside
 * int64_t. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static inline int64_t imin(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t min_path_sum(int64_t m, int64_t n, int64_t k) {
    int64_t cols = n;

    int64_t *dp = (int64_t *)malloc((size_t)cols * sizeof(int64_t));
    for (int64_t j = 0; j < cols; j++) {
        int64_t cost = ((j * 3 + k) % 13) + 1;   /* i == 0 */
        dp[j] = (j == 0) ? cost : dp[j - 1] + cost;
    }

    for (int64_t i = 1; i < m; i++) {
        dp[0] = dp[0] + (((i * 7 + k) % 13) + 1);
        for (int64_t c = 1; c < cols; c++) {
            int64_t cost = ((i * 7 + c * 3 + k) % 13) + 1;
            dp[c] = cost + imin(dp[c], dp[c - 1]);
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
        int64_t ans = min_path_sum(m, n, k);
        acc = (acc * 131 + ans) % modulus;
    }
    printf("%lld\n", (long long)acc);
    return 0;
}

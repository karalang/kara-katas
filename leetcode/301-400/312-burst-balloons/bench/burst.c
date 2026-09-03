/* Benchmark workload for LeetCode #312 - Burst Balloons.
 *
 * Mirror of burst.kara: same interval DP, same flat table reused across
 * passes, same serial dependency between passes, same masked sink. Kept
 * algorithm-for-algorithm so the cross-language comparison is honest. */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t solve(const int64_t *a, int64_t w, int64_t *dp) {
    for (int64_t len = 2; len < w; len++) {
        for (int64_t i = 0; i < w - len; i++) {
            int64_t j = i + len;
            int64_t ai = a[i];
            int64_t aj = a[j];
            int64_t base = i * w;
            int64_t best = 0;
            for (int64_t k = i + 1; k < j; k++) {
                int64_t coins = dp[base + k] + dp[k * w + j] + ai * a[k] * aj;
                if (coins > best) best = coins;
            }
            dp[base + j] = best;
        }
    }
    return dp[w - 1];
}

int main(void) {
    const int64_t n = 300;
    const int64_t w = n + 2;
    const int64_t passes = 88;

    int64_t *a = malloc((size_t)w * sizeof(int64_t));
    if (!a) return 1;
    a[0] = 1;
    int64_t state = 987654321;
    for (int64_t i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        a[i + 1] = 1 + state % 50;
    }
    a[w - 1] = 1;

    int64_t *dp = calloc((size_t)(w * w), sizeof(int64_t));
    if (!dp) return 1;

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t idx = 1 + checksum % n;
        a[idx] = 1 + (a[idx] + checksum) % 50;
        int64_t total = solve(a, w, dp);
        checksum = (checksum + total) & 1073741823;
    }

    printf("checksum %lld\n", (long long)checksum);
    free(dp);
    free(a);
    return 0;
}

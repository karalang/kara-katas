/* Benchmark harness for LeetCode #279 — Perfect Squares.
 * Mirrors perfect_squares.kara algorithm-for-algorithm.
 *
 * The other four languages allocate a fresh growable vector per call, so this
 * one does the same with malloc + realloc doubling rather than reusing one
 * static buffer. */

#include <stdio.h>
#include <stdlib.h>

static long long num_squares(long long n) {
    long long cap = 4;
    long long len = 0;
    long long *dp = malloc(sizeof(long long) * (size_t)cap);
    dp[len++] = 0;

    for (long long i = 1; i <= n; i++) {
        long long best = i;
        for (long long j = 1; j * j <= i; j++) {
            long long cand = dp[i - j * j] + 1;
            if (cand < best) {
                best = cand;
            }
        }
        if (len == cap) {
            cap *= 2;
            dp = realloc(dp, sizeof(long long) * (size_t)cap);
        }
        dp[len++] = best;
    }
    long long r = dp[n];
    free(dp);
    return r;
}

int main(void) {
    const long long iters = 100;

    long long sink = 0;
    for (long long it = 0; it < iters; it++) {
        long long n = 25000 + (it * 37) % 5001;
        sink = (sink * 31 + num_squares(n)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

/* Benchmark harness for LeetCode #264 — Ugly Number II.
 * Mirrors ugly_number_ii.kara algorithm-for-algorithm.
 *
 * The Kara/Rust/Go versions allocate a fresh growable Vec per call, so this
 * one does the same with malloc + realloc doubling rather than reusing one
 * static buffer — otherwise C would skip the allocation half of the workload
 * that the other four all pay. */

#include <stdio.h>
#include <stdlib.h>

static long long nth_ugly(long long n) {
    long long cap = 4;
    long long len = 0;
    long long *dp = malloc(sizeof(long long) * (size_t)cap);
    dp[len++] = 1;

    long long i2 = 0, i3 = 0, i5 = 0;

    while (len < n) {
        long long c2 = dp[i2] * 2;
        long long c3 = dp[i3] * 3;
        long long c5 = dp[i5] * 5;

        long long next = c2;
        if (c3 < next) {
            next = c3;
        }
        if (c5 < next) {
            next = c5;
        }

        if (len == cap) {
            cap *= 2;
            dp = realloc(dp, sizeof(long long) * (size_t)cap);
        }
        dp[len++] = next;

        if (c2 == next) {
            i2++;
        }
        if (c3 == next) {
            i3++;
        }
        if (c5 == next) {
            i5++;
        }
    }
    long long r = dp[n - 1];
    free(dp);
    return r;
}

int main(void) {
    const long long iters = 12000;

    long long sink = 0;
    for (long long it = 0; it < iters; it++) {
        long long n = 9000 + (it * 37) % 3001;
        sink = (sink * 31 + nth_ugly(n)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

/* LeetCode #120 — C mirror, bottom-up rolling min-path DP.
 * Same algorithm + workload as triangle.kara: build one N-row triangle once, then punch the O(N^2)
 * min-path DP K=20000 times with a data-dependent seed (base-row perturbation (seed+j)%7).
 * The metal floor: a flat malloc'd long[] per triangle row, a rolling dp per rep. */
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL

static long long min_path(long long **tri, long long n, long long seed) {
    long long *dp = (long long *)malloc(sizeof(long long) * n);
    for (long long j = 0; j < n; j++) dp[j] = tri[n - 1][j] + ((seed + j) % 7);
    for (long long i = n - 2; i >= 0; i--) {
        for (long long k = 0; k <= i; k++) {
            long long a = dp[k], b = dp[k + 1];
            long long m = a < b ? a : b;
            dp[k] = tri[i][k] + m;
        }
    }
    long long r = dp[0];
    free(dp);
    return r;
}

int main(void) {
    long long nrows = 200;
    long long **tri = (long long **)malloc(sizeof(long long *) * nrows);
    for (long long i = 0; i < nrows; i++) {
        tri[i] = (long long *)malloc(sizeof(long long) * (i + 1));
        for (long long j = 0; j <= i; j++) tri[i][j] = (i * 31 + j * 17) % 100;
    }
    long long acc = 0;
    for (long long rep = 0; rep < 20000; rep++) {
        long long seed = acc % 97;
        long long mp = min_path(tri, nrows, seed);
        acc = (acc * 131 + mp) % MOD;
    }
    printf("%lld\n", acc);
    for (long long i = 0; i < nrows; i++) free(tri[i]);
    free(tri);
    return 0;
}

// Benchmark workload for LeetCode #96 — Catalan DP-table, C mirror.
// K reps of the O(n^2) DP at a data-dependent size (m = 2 + acc%18, so the trip
// count is unknowable at compile time and nothing hoists), folding each count into
// a rolling hash. malloc/free a fresh table per call, matching Kara's Vec.new.
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static long long num_trees(long long n) {
    long long *dp = malloc((size_t)(n + 1) * sizeof(long long));
    dp[0] = 1;
    for (long long k = 1; k <= n; k++) {
        long long total = 0;
        for (long long r = 1; r <= k; r++) total += dp[r - 1] * dp[k - r];
        dp[k] = total;
    }
    long long res = dp[n];
    free(dp);
    return res;
}

int main(void) {
    long long acc = 1;
    for (long long rep = 0; rep < 5000000; rep++) {
        long long m = 2 + (acc % 18);
        long long c = num_trees(m);
        acc = (acc * 1000003 + c) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}

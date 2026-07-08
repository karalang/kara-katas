/*
 * Benchmark workload — Sqrt(x) (LeetCode #69).
 * C mirror of bench/sqrtx.kara. The ★'s binary search for floor(sqrt(x)) run
 * K=3_000_000 times over a Knuth-multiplicative sweep of x across [0, 2^31),
 * folding results into a rolling polynomial hash. No allocation — a pure
 * compute/branch benchmark of the search loop (int64 mid*mid <= x per step).
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t my_sqrt(int64_t x) {
    int64_t lo = 0, hi = x, ans = 0;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (mid * mid <= x) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return ans;
}

int main(void) {
    const int64_t total = 3000000;
    const int64_t modulus = 1000000007;
    const int64_t range = 2147483648LL; /* 2^31 */

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t x = (k * 2654435761LL) % range;
        int64_t r = my_sqrt(x);
        acc = (acc * 131 + r) % modulus;
    }
    printf("%lld\n", (long long)acc);
    return 0;
}

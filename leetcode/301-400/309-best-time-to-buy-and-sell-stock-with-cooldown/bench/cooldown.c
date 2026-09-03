/* Benchmark mirror — LeetCode 309, Best Time to Buy and Sell Stock with Cooldown.
 * Same three-state DP, same LCG series, same per-pass perturbation and masked
 * sink as cooldown.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 200000, passes = 1900;
    int64_t *prices = malloc((size_t)n * sizeof(int64_t));
    int64_t state = 20309;
    for (int64_t i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        prices[i] = state % 2001 - 1000;
    }

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t slot = p % n;
        prices[slot] = prices[slot] + (checksum & 1);

        int64_t hold = -prices[0], sold = 0, rest = 0;
        for (int64_t i = 1; i < n; i++) {
            int64_t prev_hold = hold, prev_sold = sold, prev_rest = rest;
            hold = prev_hold;
            if (prev_rest - prices[i] > hold) hold = prev_rest - prices[i];
            sold = prev_hold + prices[i];
            rest = prev_rest;
            if (prev_sold > rest) rest = prev_sold;
        }
        int64_t best = rest;
        if (sold > best) best = sold;
        checksum = (checksum + best) & 0x3FFFFFFF;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}

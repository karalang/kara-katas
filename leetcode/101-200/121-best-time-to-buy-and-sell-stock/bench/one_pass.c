/*
 * LeetCode 121 — one-pass Best Time to Buy and Sell Stock, C mirror.
 * Algorithmic peer of bench/one_pass.{kara,rs,py}. Same N, K, same
 * deterministic LCG generator, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t max_profit(const int64_t *prices, size_t n) {
    if (n == 0) {
        return 0;
    }
    int64_t min_price = prices[0];
    int64_t best = 0;
    for (size_t i = 1; i < n; i++) {
        int64_t p = prices[i];
        if (p < min_price) {
            min_price = p;
        }
        int64_t profit = p - min_price;
        if (profit > best) {
            best = profit;
        }
    }
    return best;
}

int main(void) {
    const size_t N = 2000000;

    int64_t *data = (int64_t *)malloc(N * sizeof(int64_t));
    int64_t state = 12345;
    for (size_t i = 0; i < N; i++) {
        state = (state * 1103515245LL + 12345LL) & 2147483647LL;
        data[i] = (state & 4095) + 1;
    }

    int64_t sum = 0;
    for (int k = 0; k < 10; k++) {
        sum += max_profit(data, N);
    }
    printf("%lld\n", (long long)sum);

    free(data);
    return 0;
}

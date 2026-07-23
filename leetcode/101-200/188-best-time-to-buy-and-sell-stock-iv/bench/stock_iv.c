#include <stdio.h>
#include <stdlib.h>

static long max_i64(long a, long b) { return a > b ? a : b; }

static long max_profit(long k, const long *prices, long n) {
    if (n == 0 || k == 0) {
        return 0;
    }
    if (k >= n / 2) {
        long profit = 0;
        for (long i = 1; i < n; i++) {
            if (prices[i] > prices[i - 1]) {
                profit += prices[i] - prices[i - 1];
            }
        }
        return profit;
    }

    long neg = -1000000000;
    long *buy = malloc((size_t)(k + 1) * sizeof(long));
    long *sell = malloc((size_t)(k + 1) * sizeof(long));
    for (long j = 0; j <= k; j++) {
        buy[j] = neg;
        sell[j] = 0;
    }
    for (long d = 0; d < n; d++) {
        long price = prices[d];
        for (long t = 1; t <= k; t++) {
            buy[t] = max_i64(buy[t], sell[t - 1] - price);
            sell[t] = max_i64(sell[t], buy[t] + price);
        }
    }
    long ans = sell[k];
    free(buy);
    free(sell);
    return ans;
}

int main(void) {
    long n = 2000;
    long kmax = 50;
    long rounds = 5000;

    long *prices = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        prices[i] = (state >> 16) % 1000;
    }

    long sink = 0;
    for (long round = 0; round < rounds; round++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long k = 1 + state % kmax;
        state = (state * 1103515245 + 12345) & 2147483647;
        long idx = state % n;
        prices[idx] = (state >> 16) % 1000;
        sink += max_profit(k, prices, n);
    }
    printf("%ld\n", sink);
    free(prices);
    return 0;
}

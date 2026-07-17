/* Benchmark workload — at-most-two-transactions DP, Best Time to Buy and Sell Stock III.
 * Algorithmic mirror of bench/max_profit.kara. See ../README.md § Benchmarks for N / K and the LCG. */
#include <stdio.h>
#include <stdlib.h>

static long long max_profit(const long long *prices, long long n) {
    if (n == 0) return 0;
    long long buy1 = -prices[0], sell1 = 0, buy2 = -prices[0], sell2 = 0;
    for (long long i = 1; i < n; i++) {
        long long p = prices[i];
        if (-p > buy1) buy1 = -p;
        if (buy1 + p > sell1) sell1 = buy1 + p;
        if (sell1 - p > buy2) buy2 = sell1 - p;
        if (buy2 + p > sell2) sell2 = buy2 + p;
    }
    return sell2;
}

int main(void) {
    long long n = 2000000;
    long long *data = (long long *)malloc(sizeof(long long) * n);
    long long state = 12345;
    for (long long i = 0; i < n; i++) { state = (state * 1103515245 + 12345) & 2147483647; data[i] = (state & 4095) + 1; }
    long long sum = 0;
    for (int k = 0; k < 10; k++) {
        long long r = max_profit(data, n);
        sum += r;
        data[0] = ((data[0] + r) & 4095) + 1;
    }
    printf("%lld\n", sum);
    free(data);
    return 0;
}

/* Benchmark workload — greedy O(n) Best Time to Buy and Sell Stock II.
 * Algorithmic mirror of bench/max_profit.kara. See ../README.md § Benchmarks for N / K and the LCG.
 * The metal floor: a flat malloc'd long[]. */
#include <stdio.h>
#include <stdlib.h>

static long long max_profit(const long long *prices, long long n) {
    long long profit = 0;
    for (long long i = 1; i < n; i++) {
        long long d = prices[i] - prices[i - 1];
        if (d > 0) profit += d;
    }
    return profit;
}

int main(void) {
    long long n = 2000000;
    long long *data = (long long *)malloc(sizeof(long long) * n);
    long long state = 12345;
    for (long long i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        data[i] = (state & 4095) + 1;
    }
    long long sum = 0;
    for (int k = 0; k < 10; k++) sum += max_profit(data, n);
    printf("%lld\n", sum);
    free(data);
    return 0;
}

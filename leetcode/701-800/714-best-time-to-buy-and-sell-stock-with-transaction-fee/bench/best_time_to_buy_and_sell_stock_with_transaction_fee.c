// LeetCode #714: Best Time to Buy and Sell Stock with Transaction Fee
// -- two running states. Benchmark mirror of the Kara star arm: the
// best cash holding no share and the best holding one, day by day.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t max_profit(const int64_t *prices, int64_t n, int64_t fee) {
    int64_t cash = 0, hold = -prices[0];
    for (int64_t i = 1; i < n; i++) {
        int64_t sold = hold + prices[i] - fee;
        if (sold > cash) cash = sold;
        int64_t bought = cash - prices[i];
        if (bought > hold) hold = bought;
    }
    return cash;
}

int main(void) {
    int64_t seed = 714;
    enum { N = 100000 };
    int64_t *walks[10];
    for (int w = 1; w <= 10; w++) {
        int64_t step = 10 * w, price = 50000;
        walks[w - 1] = malloc(N * sizeof(int64_t));
        for (int i = 0; i < N; i++) {
            price += next_random(&seed) % (2 * step + 1) - step;
            if (price < 1) price = 1;
            walks[w - 1][i] = price;
        }
    }
    int64_t sum = 0;
    for (int round = 0; round < 300; round++) {
        int64_t fee = 3 * round;
        for (int w = 0; w < 10; w++) sum += max_profit(walks[w], N, fee);
    }
    for (int w = 0; w < 10; w++) free(walks[w]);
    printf("300 rounds of 10 walks of 100000 days: sum %lld\n", (long long)sum);
    return 0;
}

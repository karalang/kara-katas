// LeetCode #2291: Maximum Profit From Trading Stocks -- the bench, the ★
// arm in C. A 0/1 knapsack row over the budget, run downwards for each
// stock that gains.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { MARKETS = 100, N = 500, BUDGET = 1000 };

static int64_t maximum_profit(const int64_t *present, const int64_t *future, int n, int64_t budget, int64_t *best) {
    for (int64_t b = 0; b <= budget; b++) best[b] = 0;
    for (int i = 0; i < n; i++) {
        int64_t cost = present[i];
        int64_t gain = future[i] - present[i];
        if (gain <= 0) continue;
        for (int64_t b = budget; b >= cost; b--) {
            int64_t with = best[b - cost] + gain;
            if (with > best[b]) best[b] = with;
        }
    }
    return best[budget];
}

static int64_t seed = 2291;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t present[MARKETS][N], future[MARKETS][N];
    for (int m = 0; m < MARKETS; m++)
        for (int i = 0; i < N; i++) {
            present[m][i] = next_random() % 101;
            future[m][i] = next_random() % 101;
        }
    int64_t *best = malloc(sizeof(int64_t) * (BUDGET + 1));
    int64_t check = 0;
    for (int m = 0; m < MARKETS; m++) check = (check * 31 + maximum_profit(present[m], future[m], N, BUDGET, best)) % 1000000007;
    printf("100 markets of 500 stocks, budget 1000: checksum %lld\n", (long long)check);
    free(best);
    return 0;
}

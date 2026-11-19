// LeetCode #1648: Sell Diminishing-Valued Colored Balls -- the bench's C
// mirror: the ★ arm on 100 random inventories of 100000 colors with up to
// 10^9 balls each, and an order for up to 10^9 of them, all drawn first.
// The counts are copied and sorted per call, as the other languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CASES 100
#define COLORS 100000
#define MOD 1000000007LL

static int descending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x < y) - (x > y);
}

static int64_t series(int64_t high, int64_t stop, int64_t width) {
    return (high + stop + 1) * (high - stop) / 2 % MOD * width % MOD;
}

static int32_t max_profit(const int32_t *inventory, size_t n, int32_t orders32) {
    int64_t *counts = malloc((n + 1) * sizeof *counts);
    for (size_t i = 0; i < n; i++) counts[i] = inventory[i];
    qsort(counts, n, sizeof *counts, descending);
    counts[n] = 0;
    int64_t orders = orders32, profit = 0;
    for (size_t i = 0; i < n; i++) {
        int64_t width = (int64_t)i + 1;
        int64_t high = counts[i], low = counts[i + 1];
        if (high == low) continue;
        if (width * (high - low) < orders) {
            profit = (profit + series(high, low, width)) % MOD;
            orders -= width * (high - low);
        } else {
            int64_t rows = orders / width, rest = orders % width;
            profit = (profit + series(high, high - rows, width)) % MOD;
            profit = (profit + rest * (high - rows) % MOD) % MOD;
            break;
        }
    }
    free(counts);
    return (int32_t)profit;
}

static int64_t seed = 1648;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t inventory[CASES][COLORS];
    int32_t orders[CASES];
    for (int c = 0; c < CASES; c++) {
        for (int i = 0; i < COLORS; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            inventory[c][i] = (int32_t)((a * 32768 + b) % 1000000000 + 1);
        }
        int64_t a = next_random();
        int64_t b = next_random();
        orders[c] = (int32_t)((a * 32768 + b) % 1000000000 + 1);
    }
    int64_t check = 0, total = 0;
    for (int c = 0; c < CASES; c++) {
        int64_t profit = max_profit(inventory[c], COLORS, orders[c]);
        total += profit;
        check = (check * 31 + profit + 1) % 1000000007;
    }
    printf("100 inventories of 100000 colors: profits sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}

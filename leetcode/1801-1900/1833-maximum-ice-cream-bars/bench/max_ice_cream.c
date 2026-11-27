// LeetCode #1833: Maximum Ice Cream Bars -- the bench in C: the ★ arm over
// 1000 calls on the first 50000 to 99999 of one list of 10^5 bars of 1 to 10^5
// coins, built once, with 10^6 to 10^8 coins, each run's length and coins
// drawn from the checksum so far. Each call copies its run, as the arm takes
// its list by value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t max_ice_cream(const int64_t *costs, int64_t n, int64_t coins) {
    int64_t dearest = costs[0];
    for (int64_t i = 1; i < n; i++)
        if (costs[i] > dearest) dearest = costs[i];
    int64_t *count = calloc((size_t)(dearest + 1), sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[costs[i]]++;
    int64_t left = coins, bars = 0;
    for (int64_t price = 1; price <= dearest; price++) {
        if (price > left) break;
        int64_t bought = count[price] < left / price ? count[price] : left / price;
        bars += bought;
        left -= bought * price;
    }
    free(count);
    return bars;
}

static int64_t seed = 1833;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *base = malloc(100000 * sizeof(int64_t));
    for (int64_t i = 0; i < 100000; i++) {
        int64_t hi = next_random();
        base[i] = 1 + (hi * 32768 + next_random()) % 100000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000; call++) {
        int64_t n = 50000 + (check + call) % 50000;
        int64_t coins = 1000000 + (check * 7 + call) % 99000000;
        int64_t *run = malloc((size_t)n * sizeof(int64_t));
        memcpy(run, base, (size_t)n * sizeof(int64_t));
        check = (check * 31 + max_ice_cream(run, n, coins)) % 1000000007;
        free(run);
    }
    printf("1000 calls: checksum %lld\n", (long long)check);
    free(base);
    return 0;
}

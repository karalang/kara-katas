// LeetCode #2706: Buy Two Chocolates -- the bench (chocolates.kara in C):
// one pass keeping the two cheapest prices.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t buy_choco(const int64_t *prices, int n, int64_t money) {
    int64_t first = 101, second = 101;
    for (int i = 0; i < n; i++) {
        int64_t p = prices[i];
        if (p < first) {
            second = first;
            first = p;
        } else if (p < second) {
            second = p;
        }
    }
    int64_t cost = first + second;
    return cost <= money ? money - cost : money;
}

static int64_t seed = 2706;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int lists = 100000, rounds = 10;
    int64_t *prices = malloc(sizeof(int64_t) * lists * 50);
    int64_t *money = malloc(sizeof(int64_t) * lists);
    for (int l = 0; l < lists; l++) {
        for (int i = 0; i < 50; i++) prices[l * 50 + i] = next_random() % 100 + 1;
        money[l] = next_random() % 100 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int l = 0; l < lists; l++) {
            int64_t left = buy_choco(prices + l * 50, 50, money[l]);
            sum += left;
            check = (check * 31 + left + r) % 1000000007;
        }
    }
    printf("%d lists of 50 prices, %d rounds: money left sums to %lld, checksum %lld\n", lists, rounds, (long long)sum, (long long)check);
    free(prices);
    free(money);
    return 0;
}

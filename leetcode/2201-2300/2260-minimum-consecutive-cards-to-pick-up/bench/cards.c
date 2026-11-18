// LeetCode #2260: Minimum Consecutive Cards to Pick Up -- C mirror of the
// ★ arm: where each value was last seen, every repeat a candidate run.
// The ★ arm's `Map` is an open-addressing hash table here, sized to the
// next power of two above twice the hand. Same workload and checksum as
// cards.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2260;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_card_pickup(const int64_t *cards, int64_t n) {
    int64_t cap = 1;
    while (cap < 2 * n) cap <<= 1;
    int64_t *keys = malloc(sizeof(int64_t) * cap);
    int64_t *vals = malloc(sizeof(int64_t) * cap);
    for (int64_t k = 0; k < cap; k++) keys[k] = -1;
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        uint64_t h = (uint64_t)cards[i] * 0x9E3779B97F4A7C15ULL;
        int64_t slot = (int64_t)(h >> 20) & (cap - 1);
        while (keys[slot] != -1 && keys[slot] != cards[i]) slot = (slot + 1) & (cap - 1);
        if (keys[slot] == cards[i]) {
            int64_t run = i - vals[slot] + 1;
            if (best < 0 || run < best) best = run;
        }
        keys[slot] = cards[i];
        vals[slot] = i;
    }
    free(keys);
    free(vals);
    return best;
}

int main(void) {
    int64_t tops[3] = {1000000, 100000, 10000};
    int64_t *cards = malloc(sizeof(int64_t) * 100000);
    int64_t check = 0;
    for (int t = 0; t < 300; t++) {
        for (int i = 0; i < 100000; i++) {
            int64_t hi = next_random();
            cards[i] = (hi * 32768 + next_random()) % tops[t % 3];
        }
        check = (check * 31 + minimum_card_pickup(cards, 100000) + 2) % 1000000007;
    }
    printf("300 hands of 10^5 cards: checksum %lld\n", (long long)check);
    free(cards);
    return 0;
}

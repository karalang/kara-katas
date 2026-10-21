// Benchmark for #822: Card Flipping Game -- the ★ arm (a set of the doubles).
//
// Mirrors flipgame.kara: the numbers on both sides of one card go in a
// set, and the answer is the smallest number on any card that is not in
// it, or 0. C has no hash set, so this one is open addressing over the
// numbers, which are never 0, with a multiplicative hash.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static uint64_t slot_of(int64_t x, int64_t cap) {
    return ((uint64_t)x * 11400714819323198485ULL) >> 32 & (uint64_t)(cap - 1);
}

static void insert(int64_t *table, int64_t cap, int64_t x) {
    uint64_t i = slot_of(x, cap);
    while (table[i] != 0 && table[i] != x) i = (i + 1) & (uint64_t)(cap - 1);
    table[i] = x;
}

static int contains(const int64_t *table, int64_t cap, int64_t x) {
    uint64_t i = slot_of(x, cap);
    while (table[i] != 0) {
        if (table[i] == x) return 1;
        i = (i + 1) & (uint64_t)(cap - 1);
    }
    return 0;
}

static int64_t flipgame(const int64_t *fronts, const int64_t *backs, int64_t n) {
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    int64_t *doubles = calloc((size_t)cap, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        if (fronts[i] == backs[i]) insert(doubles, cap, fronts[i]);
    }
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t pair[2] = {fronts[i], backs[i]};
        for (int k = 0; k < 2; k++) {
            int64_t x = pair[k];
            if (!contains(doubles, cap, x) && (best == 0 || x < best)) best = x;
        }
    }
    free(doubles);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 50000;
    int64_t seed = 822;
    int64_t *fronts[64], *backs[64];
    for (int64_t g = 0; g < count; g++) {
        fronts[g] = malloc(1000 * sizeof(int64_t));
        backs[g] = malloc(1000 * sizeof(int64_t));
        for (int64_t i = 0; i < 1000; i++) {
            int64_t f = 1 + next_random(&seed) % 2000;
            fronts[g][i] = f;
            if (next_random(&seed) % 2 == 0) backs[g][i] = f;
            else backs[g][i] = 1 + next_random(&seed) % 2000;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t answer = flipgame(fronts[g], backs[g], 1000);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    printf("%lld rounds of %lld hands: total %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}

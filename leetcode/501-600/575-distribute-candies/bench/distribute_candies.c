// Benchmark for #575: C mirror of the ★ arm (a set of the types); see
// distribute_candies.kara. C has no hash set, so each call makes a fresh
// open-addressing table of 16,384 slots (a power of two at least 1.6
// times the most candies), hashing with a 64-bit multiply, and frees it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 16384

static int64_t distribute_candies(const int64_t *candy_type, int64_t n) {
    int64_t *keys = malloc(SLOTS * sizeof(int64_t));
    unsigned char *used = calloc(SLOTS, 1);
    int64_t kinds = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t c = candy_type[i];
        uint64_t h = ((uint64_t)c * 0x9E3779B97F4A7C15ull) >> 50;
        while (used[h] && keys[h] != c) {
            h = (h + 1) & (SLOTS - 1);
        }
        if (!used[h]) {
            used[h] = 1;
            keys[h] = c;
            kinds++;
        }
    }
    free(keys);
    free(used);
    return kinds < n / 2 ? kinds : n / 2;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 575;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t count = 100;
    int64_t rounds = 200;
    int64_t *cases[100];
    for (int64_t g = 0; g < count; g++) {
        int64_t types = 1 + next_random() % 10000;
        int64_t *pool = malloc(types * sizeof(int64_t));
        for (int64_t i = 0; i < types; i++) {
            int64_t high = next_random() * 32768;
            pool[i] = (high + next_random()) % 200001 - 100000;
        }
        cases[g] = malloc(10000 * sizeof(int64_t));
        for (int64_t i = 0; i < 10000; i++) {
            cases[g][i] = pool[next_random() % types];
        }
        free(pool);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t got = distribute_candies(cases[p], 10000);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld cases of 10000 candies, %lld rounds: %lld types eaten, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(cases[g]);
    }
    return 0;
}

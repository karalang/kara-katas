// LeetCode #2898: Maximum Linear Stock Score -- the bench's C mirror
// (stock.kara). C has no map: an open-addressing table of keys with a
// splitmix64 hash, cleared for every array, and the best read off it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 18)

typedef struct { int64_t key, sum; int used; } Slot;
static Slot table[CAP];

static uint64_t mix(int64_t x) {
    uint64_t z = (uint64_t)x * 0x9E3779B97F4A7C15ULL;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static int64_t max_score(const int64_t *prices, int64_t n) {
    memset(table, 0, sizeof(table));
    for (int64_t i = 0; i < n; i++) {
        int64_t key = prices[i] - i;
        uint64_t at = mix(key) & (CAP - 1);
        while (table[at].used && table[at].key != key) at = (at + 1) & (CAP - 1);
        if (!table[at].used) {
            table[at].used = 1;
            table[at].key = key;
            table[at].sum = 0;
        }
        table[at].sum += prices[i];
    }
    int64_t best = 0;
    for (int64_t at = 0; at < CAP; at++)
        if (table[at].used && table[at].sum > best) best = table[at].sum;
    return best;
}

static int64_t seed = 2898;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 20, N = 100000 };
    int64_t *cases[COUNT];
    for (int c = 0; c < COUNT; c++) {
        cases[c] = malloc(sizeof(int64_t) * N);
        for (int64_t i = 0; i < N; i++) {
            if (c % 2 == 0)
                cases[c][i] = wide() % 1000000000 + 1;
            else
                cases[c][i] = 1000000 + i - next_random() % 50;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t score = max_score(cases[c], N);
            total += score;
            check = (check * 31 + score % 1000000007 + r) % 1000000007;
        }
    printf("%d arrays of %d, %d rounds: scores total %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    for (int c = 0; c < COUNT; c++) free(cases[c]);
    return 0;
}

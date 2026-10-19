// Benchmark for #781: Rabbits in Forest -- mirror of the ★ arm (groups
// counted by answer), with the same workload as the Kāra program. C has
// no map, so the counts go in a small open-addressing hash table with
// linear probing, cleared for each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t key, count; int used; } Slot;

static int64_t num_rabbits(const int64_t *answers, int64_t n) {
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    Slot *table = calloc(cap, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        uint64_t h = (uint64_t)answers[i] * 0x9E3779B97F4A7C15ull;
        int64_t at = (int64_t)(h >> 32) & (cap - 1);
        while (table[at].used && table[at].key != answers[i]) at = (at + 1) & (cap - 1);
        if (!table[at].used) {
            table[at].used = 1;
            table[at].key = answers[i];
        }
        table[at].count++;
    }
    int64_t total = 0;
    for (int64_t at = 0; at < cap; at++) {
        if (table[at].used) {
            int64_t size = table[at].key + 1;
            total += (table[at].count + size - 1) / size * size;
        }
    }
    free(table);
    return total;
}

static int64_t seed = 781;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 64, N = 1000 };
    static int64_t forests[COUNT][N];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t top = g % 3 == 0 ? 10 : g % 3 == 1 ? 100 : 1000;
        for (int64_t i = 0; i < N; i++) forests[g][i] = next_random() % top;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 50000; round++) {
        int64_t g = (round * 7) % COUNT;
        int64_t rabbits = num_rabbits(forests[g], N);
        total += rabbits;
        checksum = (checksum * 31 + rabbits + g) % 1000000007;
    }
    printf("50000 rounds of 1000 answers: %lld rabbits, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}

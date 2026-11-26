// LeetCode #1788: Maximize the Beauty of the Garden -- the bench in C,
// mirroring maximum_beauty.kara: a prefix sum of the positives and each
// beauty's first position, in a small open-addressing hash table.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 4096

static int32_t keys[SLOTS];
static int64_t firsts[SLOTS];
static int used[SLOTS], filled[SLOTS], nfilled;

static int32_t maximum_beauty(const int32_t *flowers, int n, int64_t *positive) {
    positive[0] = 0;
    for (int i = 0; i < n; i++) positive[i + 1] = positive[i] + (flowers[i] > 0 ? flowers[i] : 0);
    for (int f = 0; f < nfilled; f++) used[filled[f]] = 0;
    nfilled = 0;
    int64_t best = INT64_MIN;
    for (int j = 0; j < n; j++) {
        int32_t v = flowers[j];
        uint32_t h = ((uint32_t)v * 2654435761u) & (SLOTS - 1);
        while (used[h] && keys[h] != v) h = (h + 1) & (SLOTS - 1);
        if (used[h]) {
            int64_t garden = 2 * (int64_t)v + positive[j] - positive[firsts[h] + 1];
            if (garden > best) best = garden;
        } else {
            used[h] = 1; keys[h] = v; firsts[h] = j; filled[nfilled++] = (int)h;
        }
    }
    return (int32_t)best;
}

static int64_t seed = 1788;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t *gardens = malloc(sizeof(int32_t) * 400 * 2000);
    for (int g = 0; g < 400; g++) {
        for (int i = 0; i < 2000; i++) gardens[g * 2000 + i] = (int32_t)(next_random() % 20001 - 10000);
        gardens[g * 2000 + 1999] = gardens[g * 2000];
    }
    int64_t *positive = malloc(sizeof(int64_t) * 2001);
    int64_t check = 0;
    for (int64_t call = 0; call < 10000; call++) {
        const int32_t *flowers = gardens + ((check + call) % 400) * 2000;
        check = (check * 31 + maximum_beauty(flowers, 2000, positive) + 1000000000) % 1000000007;
    }
    printf("10000 calls over 400 gardens: checksum %lld\n", (long long)check);
    free(gardens);
    free(positive);
    return 0;
}

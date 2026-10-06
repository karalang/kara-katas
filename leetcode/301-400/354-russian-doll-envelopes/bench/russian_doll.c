// Bench for LeetCode #354 -- C mirror of russian_doll.kara: sort by width
// ascending and height descending, then a patience-sorting LIS over heights.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 20
#define COUNT 200000

typedef struct { int64_t w, h; } Env;

static int cmp_env(const void *pa, const void *pb) {
    const Env *a = pa, *b = pb;
    if (a->w != b->w) return a->w < b->w ? -1 : 1;
    if (a->h != b->h) return a->h > b->h ? -1 : 1;
    return 0;
}

static int64_t max_envelopes(const Env *envelopes, int64_t n) {
    Env *order = malloc(sizeof(Env) * (size_t)n);
    memcpy(order, envelopes, sizeof(Env) * (size_t)n);
    qsort(order, (size_t)n, sizeof(Env), cmp_env);
    int64_t *tails = malloc(sizeof(int64_t) * (size_t)n);
    int64_t len = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t h = order[i].h, lo = 0, hi = len;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (tails[mid] < h) lo = mid + 1; else hi = mid;
        }
        tails[lo] = h;
        if (lo == len) len++;
    }
    free(order);
    free(tails);
    return len;
}

int main(void) {
    int64_t sink = 0;
    Env *envelopes = malloc(sizeof(Env) * COUNT);
    for (int64_t round = 0; round < ROUNDS; round++) {
        int64_t seed = 354 + round;
        for (int64_t i = 0; i < COUNT; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            envelopes[i].w = seed % 100000 + 1;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            envelopes[i].h = seed % 100000 + 1;
        }
        sink = (sink * 31 + max_envelopes(envelopes, COUNT) + round) % 1000000007;
    }
    free(envelopes);
    printf("%lld\n", (long long)sink);
    return 0;
}

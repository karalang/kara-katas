// LeetCode #2808: Minimum Seconds to Equalize a Circular Array -- the
// bench in C: the ★ arm over 20 arrays of 10^5 numbers from 1000 values,
// all drawn first, then each answered 20 times; the places by value in an
// open-addressing hash table of growable arrays, C having no map.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define N 100000
#define SLOTS 262144

static int64_t seed = 2808;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

typedef struct {
    int64_t key;
    int64_t *at;
    int64_t len, cap;
    int used;
} Slot;

static Slot slots[SLOTS];

static int64_t minimum_seconds(const int64_t *nums, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        uint64_t h = ((uint64_t)nums[i] * 0x9E3779B97F4A7C15ULL) >> 46;
        while (slots[h].used && slots[h].key != nums[i]) h = (h + 1) & (SLOTS - 1);
        Slot *s = &slots[h];
        if (!s->used) {
            s->used = 1;
            s->key = nums[i];
            s->len = 0;
            s->cap = 4;
            s->at = malloc(4 * sizeof(int64_t));
        }
        if (s->len == s->cap) {
            s->cap *= 2;
            s->at = realloc(s->at, s->cap * sizeof(int64_t));
        }
        s->at[s->len++] = i;
    }
    int64_t best = n;
    for (int64_t h = 0; h < SLOTS; h++) {
        Slot *s = &slots[h];
        if (!s->used) continue;
        int64_t widest = s->at[0] + n - s->at[s->len - 1];
        for (int64_t k = 1; k < s->len; k++) {
            int64_t gap = s->at[k] - s->at[k - 1];
            if (gap > widest) widest = gap;
        }
        if (widest / 2 < best) best = widest / 2;
        free(s->at);
        s->used = 0;
    }
    return best;
}

static int64_t cases[COUNT][N];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < N; i++) cases[c][i] = wide() % 1000 * 1000003 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = minimum_seconds(cases[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: seconds sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}

// Benchmark for #638: mirror of shopping_offers.kara (the ★ arm: search
// over what is still needed, with a memo keyed by the needs) on the same
// workload. C has no map, so the memo is a small open-addressing hash
// table of six-number keys that grows when half full, standing in for
// Kāra's Map.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 6
#define OFFERS 100
#define ROUNDS 800

typedef struct {
    int64_t (*keys)[N];
    int64_t *values;  // -1 marks an empty slot
    int64_t cap;
    int64_t len;
} Memo;

static uint64_t hash(const int64_t *key) {
    uint64_t x = 0;
    for (int i = 0; i < N; i++) {
        x = (x ^ (uint64_t)key[i]) * 0x100000001b3ULL;
    }
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    return x;
}

static void memo_init(Memo *m, int64_t cap) {
    m->keys = malloc(cap * sizeof(*m->keys));
    m->values = malloc(cap * sizeof(int64_t));
    for (int64_t i = 0; i < cap; i++) {
        m->values[i] = -1;
    }
    m->cap = cap;
    m->len = 0;
}

static int64_t memo_find(const Memo *m, const int64_t *key) {
    int64_t i = (int64_t)(hash(key) & (uint64_t)(m->cap - 1));
    while (m->values[i] != -1 && memcmp(m->keys[i], key, sizeof(m->keys[i])) != 0) {
        i = (i + 1) & (m->cap - 1);
    }
    return i;
}

static void memo_insert(Memo *m, const int64_t *key, int64_t value);

static void memo_grow(Memo *m) {
    Memo old = *m;
    memo_init(m, old.cap * 2);
    for (int64_t i = 0; i < old.cap; i++) {
        if (old.values[i] != -1) {
            memo_insert(m, old.keys[i], old.values[i]);
        }
    }
    free(old.keys);
    free(old.values);
}

static void memo_insert(Memo *m, const int64_t *key, int64_t value) {
    if (2 * (m->len + 1) > m->cap) {
        memo_grow(m);
    }
    int64_t i = memo_find(m, key);
    if (m->values[i] == -1) {
        memcpy(m->keys[i], key, sizeof(m->keys[i]));
        m->len += 1;
    }
    m->values[i] = value;
}

static int64_t cheapest(const int64_t *price, int64_t special[][N + 1], const int64_t *needs, Memo *memo) {
    int64_t slot = memo_find(memo, needs);
    if (memo->values[slot] != -1) {
        return memo->values[slot];
    }
    int64_t best = 0;
    for (int i = 0; i < N; i++) {
        best += needs[i] * price[i];
    }
    for (int o = 0; o < OFFERS; o++) {
        const int64_t *offer = special[o];
        int64_t rest[N];
        bool fits = true;
        bool any = false;
        for (int i = 0; i < N; i++) {
            if (offer[i] > needs[i]) {
                fits = false;
            }
            if (offer[i] > 0) {
                any = true;
            }
            rest[i] = needs[i] - offer[i];
        }
        if (fits && any) {
            int64_t cost = offer[N] + cheapest(price, special, rest, memo);
            if (cost < best) {
                best = cost;
            }
        }
    }
    memo_insert(memo, needs, best);
    return best;
}

static int64_t shopping_offers(const int64_t *price, int64_t special[][N + 1], const int64_t *needs) {
    Memo memo;
    memo_init(&memo, 16);
    int64_t paid = cheapest(price, special, needs, &memo);
    free(memo.keys);
    free(memo.values);
    return paid;
}

static int64_t seed = 638;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t prices[20][N];
static int64_t needs[20][N];
static int64_t offers[20][OFFERS][N + 1];

int main(void) {
    for (int s = 0; s < 20; s++) {
        for (int i = 0; i < N; i++) {
            prices[s][i] = 1 + next_random() % 10;
            needs[s][i] = next_random() % 5;
        }
        for (int o = 0; o < OFFERS; o++) {
            for (int i = 0; i < N; i++) {
                offers[s][o][i] = next_random() % 3;
            }
            offers[s][o][N] = next_random() % 51;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int s = (int)(round % 20);
        int64_t paid = shopping_offers(prices[s], offers[s], needs[s]);
        total += paid;
        checksum = (checksum * 31 + paid) % 1000000007;
    }
    printf("20 shops, %d rounds: total %lld, checksum %lld\n", ROUNDS, (long long)total, (long long)checksum);
    return 0;
}

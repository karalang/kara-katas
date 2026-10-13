// Benchmark for #464: mirror of can_i_win.kara (the ★ arm: search with a
// memo keyed by the bitmask of numbers used) on the same workload. C has
// no map, so the memo is a small open-addressing hash table that grows
// when half full, standing in for Kāra's Map.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;  // -1 marks an empty slot
    bool *values;
    int64_t cap;
    int64_t len;
} Memo;

static uint64_t hash(int64_t key) {
    uint64_t x = (uint64_t)key;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    return x;
}

static void memo_init(Memo *m, int64_t cap) {
    m->keys = malloc(cap * sizeof(int64_t));
    m->values = malloc(cap * sizeof(bool));
    for (int64_t i = 0; i < cap; i++) {
        m->keys[i] = -1;
    }
    m->cap = cap;
    m->len = 0;
}

static int64_t memo_find(const Memo *m, int64_t key) {
    int64_t i = (int64_t)(hash(key) & (uint64_t)(m->cap - 1));
    while (m->keys[i] != -1 && m->keys[i] != key) {
        i = (i + 1) & (m->cap - 1);
    }
    return i;
}

static void memo_insert(Memo *m, int64_t key, bool value);

static void memo_grow(Memo *m) {
    Memo old = *m;
    memo_init(m, old.cap * 2);
    for (int64_t i = 0; i < old.cap; i++) {
        if (old.keys[i] != -1) {
            memo_insert(m, old.keys[i], old.values[i]);
        }
    }
    free(old.keys);
    free(old.values);
}

static void memo_insert(Memo *m, int64_t key, bool value) {
    if (2 * (m->len + 1) > m->cap) {
        memo_grow(m);
    }
    int64_t i = memo_find(m, key);
    if (m->keys[i] == -1) {
        m->keys[i] = key;
        m->len += 1;
    }
    m->values[i] = value;
}

static bool wins_from(int64_t used, int64_t left, int64_t m, Memo *memo) {
    int64_t slot = memo_find(memo, used);
    if (memo->keys[slot] == used) {
        return memo->values[slot];
    }
    bool result = false;
    for (int64_t n = 1; n < m + 1; n++) {
        int64_t bit = (int64_t)1 << (n - 1);
        if ((used & bit) == 0 && (n >= left || !wins_from(used | bit, left - n, m, memo))) {
            result = true;
            break;
        }
    }
    memo_insert(memo, used, result);
    return result;
}

static bool can_i_win(int64_t max_choosable, int64_t desired_total) {
    if (desired_total <= 0) {
        return true;
    }
    if (max_choosable * (max_choosable + 1) / 2 < desired_total) {
        return false;
    }
    Memo memo;
    memo_init(&memo, 16);
    bool result = wins_from(0, desired_total, max_choosable, &memo);
    free(memo.keys);
    free(memo.values);
    return result;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t games = 10;
    int64_t seed = 464;
    int64_t won = 0;
    int64_t checksum = 0;
    for (int64_t game = 0; game < games; game++) {
        int64_t total = 100 + next_random(&seed) % 111;
        if (can_i_win(20, total)) {
            won += 1;
            checksum = (checksum * 31 + game + 1) % 1000000007;
        }
    }
    printf("%lld games of 1 to 20: the first player wins %lld, checksum %lld\n", (long long)games,
           (long long)won, (long long)checksum);
    return 0;
}

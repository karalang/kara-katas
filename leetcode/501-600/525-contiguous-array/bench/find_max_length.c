// Benchmark for #525: C mirror of the ★ arm (first index of each
// balance); see find_max_length.kara. C has no map of its own, so this is
// an open-addressing table with linear probing, a fresh one for every
// call as the ★ arm's `Map.new()`, doubling at half full.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef struct {
    int64_t *keys, *vals;
    unsigned char *full;
    int64_t cap, count;
} Table;

static uint64_t hash(int64_t key, int64_t cap) {
    return ((uint64_t)key * 0x9E3779B97F4A7C15ULL) & (uint64_t)(cap - 1);
}

static void table_init(Table *t, int64_t cap) {
    t->keys = malloc(cap * sizeof(int64_t));
    t->vals = malloc(cap * sizeof(int64_t));
    t->full = calloc(cap, 1);
    t->cap = cap;
    t->count = 0;
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->full);
}

static int64_t *table_get(Table *t, int64_t key) {
    for (uint64_t h = hash(key, t->cap);; h = (h + 1) & (uint64_t)(t->cap - 1)) {
        if (!t->full[h]) return NULL;
        if (t->keys[h] == key) return &t->vals[h];
    }
}

static void table_insert(Table *t, int64_t key, int64_t val);

static void grow(Table *t) {
    Table bigger;
    table_init(&bigger, t->cap * 2);
    for (int64_t i = 0; i < t->cap; i++)
        if (t->full[i]) table_insert(&bigger, t->keys[i], t->vals[i]);
    table_free(t);
    *t = bigger;
}

static void table_insert(Table *t, int64_t key, int64_t val) {
    if (2 * (t->count + 1) > t->cap) grow(t);
    uint64_t h = hash(key, t->cap);
    while (t->full[h] && t->keys[h] != key) h = (h + 1) & (uint64_t)(t->cap - 1);
    if (!t->full[h]) {
        t->full[h] = 1;
        t->keys[h] = key;
        t->count++;
    }
    t->vals[h] = val;
}

static int64_t find_max_length(const int64_t *nums, int64_t n) {
    Table first;
    table_init(&first, 16);
    table_insert(&first, 0, -1);
    int64_t balance = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        balance += nums[i] == 1 ? 1 : -1;
        int64_t *j = table_get(&first, balance);
        if (j) {
            if (i - *j > best) best = i - *j;
        } else {
            table_insert(&first, balance, i);
        }
    }
    table_free(&first);
    return best;
}

static int64_t seed = 525;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        int64_t q = 2 + a % 3;
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) arrays[a][i] = next_random() % q == 0 ? 1 : 0;
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 20; r++) {
        for (int a = 0; a < 20; a++) {
            int64_t answer = find_max_length(arrays[a], 100000);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    printf("20 arrays of 100000, 20 rounds: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}

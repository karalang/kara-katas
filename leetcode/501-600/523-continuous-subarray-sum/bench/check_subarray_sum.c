// Benchmark for #523: C mirror of the ★ arm (first index of each prefix
// remainder); see check_subarray_sum.kara. C has no map of its own, so
// this is an open-addressing table with linear probing, a fresh one for
// every call as the ★ arm's `Map.new()`, doubling at half full.
#include <stdbool.h>
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

static bool check_subarray_sum(const int64_t *nums, int64_t n, int64_t k) {
    Table first;
    table_init(&first, 16);
    table_insert(&first, 0, -1);
    int64_t rem = 0;
    bool found = false;
    for (int64_t i = 0; i < n; i++) {
        rem = (rem + nums[i]) % k;
        int64_t *j = table_get(&first, rem);
        if (j) {
            if (i - *j >= 2) {
                found = true;
                break;
            }
        } else {
            table_insert(&first, rem, i);
        }
    }
    table_free(&first);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 20 random arrays of 100,000 numbers from 1 to 20,000 (the problem's
    // longest, summing under 2^31) made once; then each checked in 10
    // rounds against a fresh k from 10,000 to 1,073,751,823.
    int64_t seed = 523, n = 100000;
    int64_t *arrays = malloc(20 * n * sizeof(int64_t));
    for (int64_t i = 0; i < 20 * n; i++) arrays[i] = 1 + next_random(&seed) % 20000;
    int64_t yes = 0, checksum = 0;
    for (int64_t round = 0; round < 10; round++)
        for (int64_t a = 0; a < 20; a++) {
            int64_t high = next_random(&seed);
            int64_t k = 10000 + high * 32768 + next_random(&seed);
            if (check_subarray_sum(&arrays[a * n], n, k)) {
                yes++;
                checksum = (checksum + (round + 1) * (a + 1)) % 1000000007;
            }
        }
    printf("20 arrays of 100000, 10 rounds: %lld true, checksum %lld\n", (long long)yes, (long long)checksum);
    free(arrays);
    return 0;
}

// Benchmark for #446: mirror of arithmetic_slices.kara (a map of
// differences per index) on 20 random arrays of 1,000 values from -500
// to 499, built once. C has no hash map, so each index gets a small
// open-addressing table (linear probing, doubled at half full) keyed by
// difference, with a 64-bit mixing hash.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int64_t *counts;
    uint8_t *used;
    int64_t cap, len;
} Table;

static uint64_t mix(int64_t key) {
    uint64_t x = (uint64_t)key;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return x;
}

static void table_init(Table *t, int64_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(cap * sizeof(int64_t));
    t->counts = malloc(cap * sizeof(int64_t));
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->counts);
    free(t->used);
}

static int64_t table_get(const Table *t, int64_t key) {
    uint64_t mask = (uint64_t)t->cap - 1;
    for (uint64_t at = mix(key) & mask;; at = (at + 1) & mask) {
        if (!t->used[at]) {
            return 0;
        }
        if (t->keys[at] == key) {
            return t->counts[at];
        }
    }
}

static void table_add(Table *t, int64_t key, int64_t amount);

static void table_grow(Table *t) {
    Table bigger;
    table_init(&bigger, t->cap * 2);
    for (int64_t i = 0; i < t->cap; i++) {
        if (t->used[i]) {
            table_add(&bigger, t->keys[i], t->counts[i]);
        }
    }
    table_free(t);
    *t = bigger;
}

static void table_add(Table *t, int64_t key, int64_t amount) {
    if ((t->len + 1) * 2 > t->cap) {
        table_grow(t);
    }
    uint64_t mask = (uint64_t)t->cap - 1;
    for (uint64_t at = mix(key) & mask;; at = (at + 1) & mask) {
        if (!t->used[at]) {
            t->used[at] = 1;
            t->keys[at] = key;
            t->counts[at] = amount;
            t->len++;
            return;
        }
        if (t->keys[at] == key) {
            t->counts[at] += amount;
            return;
        }
    }
}

static int64_t number_of_arithmetic_slices(const int64_t *nums, int64_t n) {
    Table *ending = malloc(n * sizeof(Table));
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        table_init(&ending[i], 8);
        for (int64_t j = 0; j < i; j++) {
            int64_t d = nums[i] - nums[j];
            int64_t before = table_get(&ending[j], d);
            total += before;
            table_add(&ending[i], d, before + 1);
        }
    }
    for (int64_t i = 0; i < n; i++) {
        table_free(&ending[i]);
    }
    free(ending);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 20, n = 1000;
    int64_t seed = 446;
    int64_t *arrays = malloc(count * n * sizeof(int64_t));
    for (int64_t i = 0; i < count * n; i++) {
        arrays[i] = next_random(&seed) % 1000 - 500;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < count; c++) {
        int64_t answer = number_of_arithmetic_slices(arrays + c * n, n);
        total += answer;
        checksum = (checksum * 31 + answer % 1000000007) % 1000000007;
    }
    printf("%lld arrays of %lld: %lld slices, checksum %lld\n", (long long)count, (long long)n,
           (long long)total, (long long)checksum);
    free(arrays);
    return 0;
}

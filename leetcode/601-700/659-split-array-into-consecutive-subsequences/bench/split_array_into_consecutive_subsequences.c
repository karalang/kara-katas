// Benchmark for #659: the greedy, as the Kara ★ arm. C has no map, so
// each of the two counts is a hash table of open addressing with linear
// probing, made fresh for each call and freed after it.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int64_t *values;
    bool *used;
    uint64_t mask;
} Table;

static Table table_new(uint64_t capacity) {
    Table t;
    t.keys = malloc(capacity * sizeof *t.keys);
    t.values = malloc(capacity * sizeof *t.values);
    t.used = calloc(capacity, sizeof *t.used);
    t.mask = capacity - 1;
    return t;
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->values);
    free(t->used);
}

static uint64_t mix(int64_t k) {
    uint64_t h = (uint64_t)k * 0x9E3779B97F4A7C15ull;
    return h ^ (h >> 29);
}

// The slot holding `k`, made with a count of 0 if missing.
static int64_t *slot(Table *t, int64_t k) {
    uint64_t i = mix(k) & t->mask;
    while (t->used[i] && t->keys[i] != k) i = (i + 1) & t->mask;
    if (!t->used[i]) {
        t->used[i] = true;
        t->keys[i] = k;
        t->values[i] = 0;
    }
    return &t->values[i];
}

static int64_t count(const Table *t, int64_t k) {
    uint64_t i = mix(k) & t->mask;
    while (t->used[i]) {
        if (t->keys[i] == k) return t->values[i];
        i = (i + 1) & t->mask;
    }
    return 0;
}

static bool is_possible(const int64_t *nums, int64_t n) {
    uint64_t capacity = 16;
    while (capacity < (uint64_t)n * 2) capacity *= 2;
    Table left = table_new(capacity), ends = table_new(capacity);
    for (int64_t i = 0; i < n; i++) *slot(&left, nums[i]) += 1;
    bool ok = true;
    for (int64_t i = 0; i < n && ok; i++) {
        int64_t x = nums[i];
        if (count(&left, x) == 0) continue;
        *slot(&left, x) -= 1;
        if (count(&ends, x - 1) > 0) {
            *slot(&ends, x - 1) -= 1;
            *slot(&ends, x) += 1;
        } else if (count(&left, x + 1) > 0 && count(&left, x + 2) > 0) {
            *slot(&left, x + 1) -= 1;
            *slot(&left, x + 2) -= 1;
            *slot(&ends, x + 2) += 1;
        } else {
            ok = false;
        }
    }
    table_free(&left);
    table_free(&ends);
    return ok;
}

static int64_t seed = 659;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int inputs = 8, rounds = 40;
    int64_t *arrays[8], lengths[8];
    for (int k = 0; k < inputs; k++) {
        int64_t *nums = malloc(25000 * 5 * sizeof *nums + sizeof *nums);
        int64_t n = 0;
        for (int r = 0; r < 25000; r++) {
            int64_t start = next_random() % 20001;
            int64_t length = 3 + next_random() % 3;
            for (int64_t v = start; v < start + length; v++) nums[n++] = v;
        }
        if (k % 2 == 1) nums[n++] = 30000;
        qsort(nums, n, sizeof *nums, cmp);
        arrays[k] = nums;
        lengths[k] = n;
    }
    int64_t yes = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        int pick = (r * 3) % inputs;
        bool ok = is_possible(arrays[pick], lengths[pick]);
        if (ok) yes++;
        checksum = (checksum * 31 + lengths[pick] * 2 + (ok ? 1 : 0)) % 1000000007;
    }
    printf("%d arrays, %d rounds: %lld split, checksum %lld\n", inputs, rounds, (long long)yes,
           (long long)checksum);
    for (int k = 0; k < inputs; k++) free(arrays[k]);
    return 0;
}

// LeetCode #1481: Least Number of Unique Integers after K Removals --
// bench, C mirror of find_least_num_of_unique_ints.kara. C has no map, so
// the counts are kept in an open-addressing table, linear probing over a
// multiplicative hash, grown at half full and malloc'ed each call, as the
// Kāra and Rust maps are made anew.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int32_t *keys;
    int64_t *vals;
    char *used;
    int64_t cap, len;
} Table;

static void table_init(Table *t, int64_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(sizeof(int32_t) * cap);
    t->vals = malloc(sizeof(int64_t) * cap);
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static int64_t slot(const Table *t, int32_t key) {
    uint64_t h = (uint64_t)(uint32_t)key * 0x9E3779B97F4A7C15ULL;
    int64_t i = (int64_t)(h >> 20) & (t->cap - 1);
    while (t->used[i] && t->keys[i] != key) i = (i + 1) & (t->cap - 1);
    return i;
}

static void table_add(Table *t, int32_t key) {
    if (2 * (t->len + 1) > t->cap) {
        Table bigger;
        table_init(&bigger, 2 * t->cap);
        for (int64_t i = 0; i < t->cap; i++) {
            if (t->used[i]) {
                int64_t j = slot(&bigger, t->keys[i]);
                bigger.used[j] = 1;
                bigger.keys[j] = t->keys[i];
                bigger.vals[j] = t->vals[i];
            }
        }
        bigger.len = t->len;
        table_free(t);
        *t = bigger;
    }
    int64_t i = slot(t, key);
    if (!t->used[i]) {
        t->used[i] = 1;
        t->keys[i] = key;
        t->vals[i] = 0;
        t->len++;
    }
    t->vals[i]++;
}

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int32_t find_least_num_of_unique_ints(const int32_t *arr, int64_t n, int32_t k) {
    Table t;
    table_init(&t, 16);
    for (int64_t i = 0; i < n; i++) table_add(&t, arr[i]);
    int64_t *counts = malloc(sizeof(int64_t) * t.len);
    int64_t m = 0;
    for (int64_t i = 0; i < t.cap; i++) {
        if (t.used[i]) counts[m++] = t.vals[i];
    }
    table_free(&t);
    qsort(counts, m, sizeof(int64_t), cmp_i64);
    int64_t left = k, unique = m;
    for (int64_t i = 0; i < m; i++) {
        if (counts[i] > left) break;
        left -= counts[i];
        unique--;
    }
    free(counts);
    return (int32_t)unique;
}

static int64_t seed = 1481;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 100000;
    int32_t *arr = malloc(sizeof(int32_t) * n);
    for (int64_t i = 0; i < n; i++) arr[i] = (int32_t)(1 + next_random() % 30000);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        arr[check % 100000] = (int32_t)(1 + (check / 7) % 30000);
        int32_t k = (int32_t)(check % 100000);
        check = (check * 31 + find_least_num_of_unique_ints(arr, n, k) + pass) % 1000000007;
    }
    printf("100 passes over 100000 values: checksum %lld\n", (long long)check);
    free(arr);
    return 0;
}

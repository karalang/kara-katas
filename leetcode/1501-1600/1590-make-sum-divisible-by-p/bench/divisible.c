// LeetCode #1590: Make Sum Divisible by P -- the bench in C, mirroring
// divisible.kara. C has no map: an open-addressing table of remainders
// with linear probing and a multiplicative hash, grown at half full and
// allocated per call, as Kāra's `Map` is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys, *vals;
    uint8_t *used;
    uint64_t cap, len;
} Table;

static uint64_t slot(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    uint64_t i = h & (t->cap - 1);
    while (t->used[i] && t->keys[i] != key) i = (i + 1) & (t->cap - 1);
    return i;
}

static void table_init(Table *t, uint64_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(cap * sizeof(int64_t));
    t->vals = malloc(cap * sizeof(int64_t));
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static void put(Table *t, int64_t key, int64_t val) {
    if (2 * (t->len + 1) > t->cap) {
        Table bigger;
        table_init(&bigger, t->cap * 2);
        for (uint64_t i = 0; i < t->cap; i++)
            if (t->used[i]) {
                uint64_t s = slot(&bigger, t->keys[i]);
                bigger.used[s] = 1;
                bigger.keys[s] = t->keys[i];
                bigger.vals[s] = t->vals[i];
                bigger.len++;
            }
        table_free(t);
        *t = bigger;
    }
    uint64_t s = slot(t, key);
    if (!t->used[s]) {
        t->used[s] = 1;
        t->keys[s] = key;
        t->len++;
    }
    t->vals[s] = val;
}

static int min_subarray(const int32_t *nums, int64_t n, int32_t p32) {
    int64_t p = p32;
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) sum += nums[i];
    int64_t need = sum % p;
    if (need == 0) return 0;
    Table last;
    table_init(&last, 8);
    put(&last, 0, -1);
    int64_t prefix = 0, best = n;
    for (int64_t j = 0; j < n; j++) {
        prefix = (prefix + nums[j]) % p;
        uint64_t s = slot(&last, (prefix - need + p) % p);
        if (last.used[s] && j - last.vals[s] < best) best = j - last.vals[s];
        put(&last, prefix, j);
    }
    table_free(&last);
    return best == n ? -1 : (int)best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    int64_t seed = 1590;
    int32_t *nums[40];
    int32_t ps[40];
    for (int k = 0; k < 40; k++) {
        nums[k] = malloc(100000 * sizeof(int32_t));
        for (int i = 0; i < 100000; i++) nums[k][i] = (int32_t)(wide(&seed) % 1000000000 + 1);
        ps[k] = (int32_t)(wide(&seed) % 100000 + 1);
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < 40; k++) {
        int64_t answer = min_subarray(nums[k], 100000, ps[k]);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("40 problems of 100000 values: lengths %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}

// LeetCode #2025: Maximum Number of Ways to Partition an Array -- the ★ arm
// in C, the same algorithm and workload as partition.kara: two hash tables
// of the pivots' differences (open addressing, a multiplicative hash),
// swept.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *keys;
    int64_t *counts;
    uint8_t *used;
    uint64_t mask;
} Table;

static void table_init(Table *t, int64_t n) {
    uint64_t cap = 16;
    while (cap < (uint64_t)n * 2) cap <<= 1;
    t->keys = malloc(sizeof(int64_t) * cap);
    t->counts = calloc(cap, sizeof(int64_t));
    t->used = calloc(cap, 1);
    t->mask = cap - 1;
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->counts);
    free(t->used);
}

static uint64_t slot_of(const Table *t, int64_t key) {
    uint64_t i = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 20 & t->mask;
    while (t->used[i] && t->keys[i] != key) i = (i + 1) & t->mask;
    return i;
}

static void table_add(Table *t, int64_t key, int64_t by) {
    uint64_t i = slot_of(t, key);
    if (!t->used[i]) {
        t->used[i] = 1;
        t->keys[i] = key;
    }
    t->counts[i] += by;
}

static int64_t table_get(const Table *t, int64_t key) {
    uint64_t i = slot_of(t, key);
    return t->used[i] ? t->counts[i] : 0;
}

static int64_t ways_to_partition(const int64_t *nums, int64_t n, int64_t k) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t *d = malloc(sizeof(int64_t) * n);
    int64_t left = 0;
    for (int64_t p = 1; p < n; p++) {
        left += nums[p - 1];
        d[p - 1] = left - (total - left);
    }
    Table right, seen;
    table_init(&right, n);
    table_init(&seen, n);
    for (int64_t p = 0; p < n - 1; p++) table_add(&right, d[p], 1);
    int64_t best = table_get(&right, 0);
    for (int64_t i = 0; i < n; i++) {
        if (i >= 1) {
            table_add(&right, d[i - 1], -1);
            table_add(&seen, d[i - 1], 1);
        }
        int64_t delta = k - nums[i];
        int64_t ways = table_get(&right, -delta) + table_get(&seen, delta);
        if (ways > best) best = ways;
    }
    table_free(&right);
    table_free(&seen);
    free(d);
    return best;
}

static int64_t seed = 2025;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rs[8] = {1, 2, 3, 10, 100, 1000, 10000, 100000};
    int64_t *arrays[20];
    int64_t ks[20];
    for (int a = 0; a < 20; a++) {
        int64_t r = rs[a % 8];
        arrays[a] = malloc(sizeof(int64_t) * 50000);
        for (int i = 0; i < 50000; i++) arrays[a][i] = next_random() % (2 * r + 1) - r;
        ks[a] = next_random() % (2 * r + 1) - r;
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int a = 0; a < 20; a++) {
            int64_t best = ways_to_partition(arrays[a], 50000, ks[a]);
            calls++;
            total += best;
            check = (check * 31 + best) % 1000000007;
        }
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}

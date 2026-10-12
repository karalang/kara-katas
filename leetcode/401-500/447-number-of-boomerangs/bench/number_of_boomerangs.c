// Benchmark for #447: mirror of number_of_boomerangs.kara (a map of
// distances per point) on 10 random sets of 1,000 distinct points on a
// 300 x 300 grid, built once. C has no hash map, so each point gets a
// small open-addressing table (linear probing, doubled at half full)
// keyed by squared distance, with a 64-bit mixing hash. Points are kept
// distinct with a 300 x 300 grid of flags.
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

static int64_t number_of_boomerangs(const int64_t *xs, const int64_t *ys, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        Table counts;
        table_init(&counts, 8);
        for (int64_t j = 0; j < n; j++) {
            int64_t dx = xs[i] - xs[j];
            int64_t dy = ys[i] - ys[j];
            table_add(&counts, dx * dx + dy * dy, 1);
        }
        for (int64_t k = 0; k < counts.cap; k++) {
            if (counts.used[k]) {
                total += counts.counts[k] * (counts.counts[k] - 1);
            }
        }
        table_free(&counts);
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 10, n = 1000;
    int64_t seed = 447;
    int64_t *xs = malloc(count * n * sizeof(int64_t));
    int64_t *ys = malloc(count * n * sizeof(int64_t));
    for (int64_t c = 0; c < count; c++) {
        uint8_t *seen = calloc(300 * 300, 1);
        int64_t have = 0;
        while (have < n) {
            int64_t x = next_random(&seed) % 300;
            int64_t y = next_random(&seed) % 300;
            if (!seen[x * 300 + y]) {
                seen[x * 300 + y] = 1;
                xs[c * n + have] = x;
                ys[c * n + have] = y;
                have++;
            }
        }
        free(seen);
    }
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < count; c++) {
        int64_t answer = number_of_boomerangs(xs + c * n, ys + c * n, n);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld sets of %lld points: %lld boomerangs, checksum %lld\n", (long long)count, (long long)n,
           (long long)total, (long long)checksum);
    free(xs);
    free(ys);
    return 0;
}

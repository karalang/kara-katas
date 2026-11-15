// LeetCode #1577: Number of Ways Where Square of Number Is Equal to
// Product of Two Numbers -- bench: the ★ arm (a walk with a Map of the
// values seen) over 10 pairs of arrays of 1000 values, each a power of 2
// or 3 times a factor below 100, drawn first.
// C mirror of triplets.kara: the map is an open-addressing hash table that
// doubles when half full, made anew for each value, as the other
// languages make a new library map.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys, *vals;
    bool *used;
    int64_t cap, len;
} Map;

static uint64_t hash(int64_t x) {
    uint64_t z = (uint64_t)x + 0x9e3779b97f4a7c15ULL;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

static void map_init(Map *m, int64_t cap) {
    m->cap = cap;
    m->len = 0;
    m->keys = malloc(cap * sizeof(int64_t));
    m->vals = malloc(cap * sizeof(int64_t));
    m->used = calloc(cap, sizeof(bool));
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static int64_t map_get(const Map *m, int64_t k) {
    uint64_t i = hash(k) & (m->cap - 1);
    while (m->used[i]) {
        if (m->keys[i] == k) return m->vals[i];
        i = (i + 1) & (m->cap - 1);
    }
    return 0;
}

static void map_add(Map *m, int64_t k, int64_t d);

static void map_grow(Map *m) {
    Map old = *m;
    map_init(m, old.cap * 2);
    for (int64_t i = 0; i < old.cap; i++) {
        if (old.used[i]) map_add(m, old.keys[i], old.vals[i]);
    }
    map_free(&old);
}

static void map_add(Map *m, int64_t k, int64_t d) {
    uint64_t i = hash(k) & (m->cap - 1);
    while (m->used[i]) {
        if (m->keys[i] == k) {
            m->vals[i] += d;
            return;
        }
        i = (i + 1) & (m->cap - 1);
    }
    m->used[i] = true;
    m->keys[i] = k;
    m->vals[i] = d;
    if (++m->len * 2 > m->cap) map_grow(m);
}

static int64_t ways(const int64_t *squares, int64_t n, const int64_t *products, int64_t m) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t target = squares[i] * squares[i];
        Map seen;
        map_init(&seen, 16);
        for (int64_t j = 0; j < m; j++) {
            int64_t y = products[j];
            if (target % y == 0) {
                total += map_get(&seen, target / y);
            }
            map_add(&seen, y, 1);
        }
        map_free(&seen);
    }
    return total;
}

static int64_t seed = 1577;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    static int64_t arrays[20][1000];
    for (int a = 0; a < 20; a++) {
        for (int i = 0; i < 1000; i++) {
            int64_t v = next_random() % 100 + 1;
            int64_t times = next_random() % 4;
            for (int64_t t = 0; t < times; t++) {
                v *= 2 + next_random() % 2;
            }
            arrays[a][i] = v < 100000 ? v : 100000;
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < 10; p++) {
        int64_t w = ways(arrays[2 * p], 1000, arrays[2 * p + 1], 1000) +
                    ways(arrays[2 * p + 1], 1000, arrays[2 * p], 1000);
        total += w;
        check = mix(check, w);
    }
    printf("10 pairs of arrays of 1000 values: triplets total %lld, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}

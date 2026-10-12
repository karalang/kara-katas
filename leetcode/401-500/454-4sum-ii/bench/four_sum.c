// Benchmark for #454: mirror of four_sum.kara (the ★ arm, pair sums of
// the first two arrays counted in a map) on the same workload. C has no
// map, so this one is an open-addressing table with linear probing,
// doubled when it is half full.
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int64_t *counts;  // 0 marks an empty slot
    uint64_t mask;
    int64_t len;
} Map;

static uint64_t mix(int64_t key) {
    uint64_t x = (uint64_t)key;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return x;
}

static void map_init(Map *m, uint64_t slots) {
    m->keys = malloc(slots * sizeof(int64_t));
    m->counts = calloc(slots, sizeof(int64_t));
    m->mask = slots - 1;
    m->len = 0;
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->counts);
}

static void map_add(Map *m, int64_t key, int64_t by);

static void map_grow(Map *m) {
    Map bigger;
    map_init(&bigger, (m->mask + 1) * 2);
    for (uint64_t i = 0; i <= m->mask; i++) {
        if (m->counts[i] != 0) {
            map_add(&bigger, m->keys[i], m->counts[i]);
        }
    }
    map_free(m);
    *m = bigger;
}

static void map_add(Map *m, int64_t key, int64_t by) {
    uint64_t i = mix(key) & m->mask;
    while (m->counts[i] != 0) {
        if (m->keys[i] == key) {
            m->counts[i] += by;
            return;
        }
        i = (i + 1) & m->mask;
    }
    m->keys[i] = key;
    m->counts[i] = by;
    m->len += 1;
    if ((uint64_t)m->len * 2 > m->mask + 1) {
        map_grow(m);
    }
}

static int64_t map_get(const Map *m, int64_t key) {
    uint64_t i = mix(key) & m->mask;
    while (m->counts[i] != 0) {
        if (m->keys[i] == key) {
            return m->counts[i];
        }
        i = (i + 1) & m->mask;
    }
    return 0;
}

static int64_t four_sum_count(const int64_t *nums1, const int64_t *nums2, const int64_t *nums3,
                              const int64_t *nums4, int64_t n) {
    Map sums;
    map_init(&sums, 16);
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < n; j++) {
            map_add(&sums, nums1[i] + nums2[j], 1);
        }
    }
    int64_t count = 0;
    for (int64_t k = 0; k < n; k++) {
        for (int64_t l = 0; l < n; l++) {
            count += map_get(&sums, -(nums3[k] + nums4[l]));
        }
    }
    map_free(&sums);
    return count;
}

// ---- benchmark --------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_value(int64_t *seed) {
    int64_t hi = next_random(seed);
    int64_t lo = next_random(seed);
    return (hi * 65536 + lo) % 100001 - 50000;
}

int main(void) {
    const int64_t n = 1000;
    const int64_t rounds = 10;
    int64_t seed = 454;
    int64_t *arrays[4];
    for (int a = 0; a < 4; a++) {
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = random_value(&seed);
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int a = 0; a < 4; a++) {
            int64_t at = next_random(&seed) % n;
            arrays[a][at] = random_value(&seed);
        }
        int64_t tuples = four_sum_count(arrays[0], arrays[1], arrays[2], arrays[3], n);
        total += tuples;
        checksum = (checksum * 31 + tuples) % 1000000007;
    }
    printf("%" PRId64 " rounds on 4 arrays of %" PRId64 ": %" PRId64 " tuples, checksum %" PRId64 "\n", rounds, n,
           total, checksum);
    for (int a = 0; a < 4; a++) {
        free(arrays[a]);
    }
    return 0;
}

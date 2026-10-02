/* Benchmark workload for LeetCode #325 — C mirror of max_sub_len.kara.
 *
 * C has no standard hash map, so one is written here, shaped like the Kara
 * runtime's `Map[K, V]` rather than tuned to this workload:
 *
 *   - heap-allocated per call, like the kata's `Map.new()`, freed on return;
 *   - capacity 16 to start, a power of two, linear probing;
 *   - doubles and rehashes when (len + 1) * 4 > capacity * 3, the runtime's
 *     75% load factor;
 *   - SipHash-1-3 over the key's 8 bytes, which is the hash Kara's default
 *     `Map` and Rust's `HashMap` both use. The key is fixed here instead of
 *     drawn per process; that changes which buckets are hit, not the work.
 *
 * Not modelled: the runtime's 7-bit tag in the control byte. With an i64 key
 * a full key compare is as cheap as a tag compare, so it would buy nothing.
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 200000
#define PUNCHES 60
#define MODULUS 1073741789LL
#define INITIAL_CAPACITY 16

static const uint64_t K0 = 0x0706050403020100ULL;
static const uint64_t K1 = 0x0f0e0d0c0b0a0908ULL;

#define ROTL(x, b) (uint64_t)(((x) << (b)) | ((x) >> (64 - (b))))
#define SIPROUND                                                       \
    do {                                                               \
        v0 += v1; v1 = ROTL(v1, 13); v1 ^= v0; v0 = ROTL(v0, 32);      \
        v2 += v3; v3 = ROTL(v3, 16); v3 ^= v2;                         \
        v0 += v3; v3 = ROTL(v3, 21); v3 ^= v0;                         \
        v2 += v1; v1 = ROTL(v1, 17); v1 ^= v2; v2 = ROTL(v2, 32);      \
    } while (0)

/* SipHash-1-3 of one 8-byte little-endian message. */
static inline uint64_t siphash13_u64(uint64_t m) {
    uint64_t v0 = K0 ^ 0x736f6d6570736575ULL;
    uint64_t v1 = K1 ^ 0x646f72616e646f6dULL;
    uint64_t v2 = K0 ^ 0x6c7967656e657261ULL;
    uint64_t v3 = K1 ^ 0x7465646279746573ULL;
    v3 ^= m;
    SIPROUND;
    v0 ^= m;
    uint64_t b = (uint64_t)8 << 56;
    v3 ^= b;
    SIPROUND;
    v0 ^= b;
    v2 ^= 0xff;
    SIPROUND;
    SIPROUND;
    SIPROUND;
    return v0 ^ v1 ^ v2 ^ v3;
}

typedef struct {
    int64_t *key;
    int64_t *val;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->key = malloc(m->cap * sizeof(int64_t));
    m->val = malloc(m->cap * sizeof(int64_t));
    m->used = calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->key);
    free(m->val);
    free(m->used);
}

static size_t map_slot(const Map *m, int64_t k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)siphash13_u64((uint64_t)k) & mask;
    while (m->used[h] && m->key[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static void map_grow(Map *m) {
    int64_t *ok = m->key, *ov = m->val;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;
    m->cap = ocap * 2;
    m->key = malloc(m->cap * sizeof(int64_t));
    m->val = malloc(m->cap * sizeof(int64_t));
    m->used = calloc(m->cap, 1);
    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(m, ok[i]);
            m->used[h] = 1;
            m->key[h] = ok[i];
            m->val[h] = ov[i];
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

/* Insert k -> v only if k is absent (`entry(k).or_insert(v)`). */
static void map_insert_absent(Map *m, int64_t k, int64_t v) {
    size_t h = map_slot(m, k);
    if (m->used[h]) {
        return;
    }
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        h = map_slot(m, k);
    }
    m->used[h] = 1;
    m->key[h] = k;
    m->val[h] = v;
    m->len++;
}

static int64_t max_sub_len(const int64_t *nums, int64_t n, int64_t k) {
    Map first;
    map_init(&first);
    map_insert_absent(&first, 0, -1);
    int64_t p = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        p += nums[i];
        size_t h = map_slot(&first, p - k);
        if (first.used[h] && i - first.val[h] > best) {
            best = i - first.val[h];
        }
        map_insert_absent(&first, p, i);
    }
    map_free(&first);
    return best;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 325;
    const int64_t ranges[3] = {1, 100, 10000};
    int64_t *arrays[3];
    for (int t = 0; t < 3; t++) {
        int64_t r = ranges[t];
        arrays[t] = malloc(LEN * sizeof(int64_t));
        for (int64_t i = 0; i < LEN; i++) {
            arrays[t][i] = next(&seed) % (2 * r + 1) - r;
        }
    }

    int64_t sink = 0;
    for (int64_t punch = 0; punch < PUNCHES; punch++) {
        int t = (int)(punch % 3);
        int64_t r = ranges[t];
        int64_t hi = next(&seed);
        int64_t pos = (hi * 32768 + next(&seed)) % LEN;
        arrays[t][pos] = next(&seed) % (2 * r + 1) - r;
        int64_t k = (next(&seed) % 41 - 20) * r / 4;
        int64_t len = max_sub_len(arrays[t], LEN, k);
        sink = (sink * 31 + len + 1) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    for (int t = 0; t < 3; t++) {
        free(arrays[t]);
    }
    return 0;
}

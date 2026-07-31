/*
 * LeetCode 3 — sliding-window O(n) Longest Substring Without Repeating
 * Characters, bench mirror in C.
 *
 * Algorithmic mirror of bench/sliding_window.{kara,rs,py}. Same input:
 * the 26-character lowercase alphabet repeated 4000 times for a
 * 104_000-char string. K=20 outer iterations. Stdout sink: K * 26 = 520.
 *
 * C has no hashmap in libc, so this carries an open-addressing,
 * linear-probing hashmap keyed by i32 codepoint with i64 indices. The table
 * is shaped to match the runtime's Map[K,V] rather than presized to the
 * workload:
 *
 *   - heap-allocated per call, like the kata's `Map.new()` per
 *     `length_of_longest_substring` invocation, and freed on the way out;
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply), replacing the
 *     splitmix mixer this mirror used.
 *
 * The previous fixed 64-entry static table was presized to just past the
 * 26-key working set and merely memset per call, so it never allocated, grew,
 * or rehashed, while the kata's map climbs 16 -> 32 -> 64. Presizing to the
 * answer is not a C advantage, it is a different program.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    int32_t *keys;
    int64_t *vals;
    bool *used;
    size_t cap;
    size_t len;
} Map;

static inline uint64_t fxhash_key(int32_t k) {
    return (uint64_t)(uint32_t)k * FXHASH_SEED;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = malloc(m->cap * sizeof(int32_t));
    m->vals = malloc(m->cap * sizeof(int64_t));
    m->used = calloc(m->cap, sizeof(bool));
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static size_t map_slot(const Map *m, int32_t k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_key(k) & mask;
    while (m->used[h] && m->keys[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static bool map_get(const Map *m, int32_t k, int64_t *out) {
    size_t h = map_slot(m, k);
    if (!m->used[h]) return false;
    *out = m->vals[h];
    return true;
}

static void map_grow(Map *m) {
    int32_t *ok = m->keys;
    int64_t *ov = m->vals;
    bool *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->keys = malloc(m->cap * sizeof(int32_t));
    m->vals = malloc(m->cap * sizeof(int64_t));
    m->used = calloc(m->cap, sizeof(bool));

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(m, ok[i]);
            m->used[h] = true;
            m->keys[h] = ok[i];
            m->vals[h] = ov[i];
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

static void map_insert(Map *m, int32_t k, int64_t v) {
    size_t h = map_slot(m, k);
    if (m->used[h]) {
        m->vals[h] = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        h = map_slot(m, k);
    }
    m->used[h] = true;
    m->keys[h] = k;
    m->vals[h] = v;
    m->len++;
}

static int64_t length_of_longest_substring(const char *s, size_t n) {
    Map m;
    map_init(&m);
    int64_t left = 0;
    int64_t best = 0;
    for (size_t right = 0; right < n; right++) {
        int32_t c = (int32_t)(unsigned char)s[right];
        int64_t prev;
        if (map_get(&m, c, &prev) && prev >= left) {
            left = prev + 1;
        }
        map_insert(&m, c, (int64_t)right);
        int64_t window = (int64_t)right - left + 1;
        if (window > best) best = window;
    }
    map_free(&m);
    return best;
}

int main(void) {
    const size_t N = 104000;   /* 26 * 4000 */
    char *data = (char *)malloc(N + 1);
    const char *alpha = "abcdefghijklmnopqrstuvwxyz";
    for (size_t i = 0; i < N; i++) data[i] = alpha[i % 26];
    data[N] = '\0';

    int64_t sum = 0;
    for (int k = 0; k < 20; k++) {
        sum += length_of_longest_substring(data, N);
    }
    printf("%lld\n", (long long)sum);
    free(data);
    return 0;
}

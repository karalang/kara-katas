/*
 * LeetCode 1 — hash-map O(n) Two Sum, bench mirror in C.
 *
 * Algorithmic mirror of bench/hash_map.kara and bench/hash_map.rs. Same
 * N=5000, K=10, sentinel target=-1 (never matches; full pass per call).
 * Stdout sink: K * (-1 + -1) = -20.
 *
 * C has no hashmap in libc, so this carries one. It is written to match what
 * `Map[i64, i64]` ACTUALLY DOES, because the previous version did not and the
 * gap was large enough to invalidate the comparison: kāra measured 83x behind
 * this mirror, the worst deficit in the corpus, and most of that was the two
 * sides not being the same data structure.
 *
 * The three properties that matter, all now matched to runtime/src/map.rs:
 *
 *   1. HEAP storage, allocated and freed per `two_sum` call — the kāra source
 *      says `let mut seen: Map[i64, i64] = Map.new();` inside the function, so
 *      it pays a fresh allocation every call. The old mirror used `static`
 *      arrays and paid none.
 *   2. GROWS from a small initial capacity. kāra starts at INITIAL_CAPACITY=16
 *      and resizes when `(len + tombstones + 1) * 4 > capacity * 3` (a 75% load
 *      factor), so filling 5000 entries costs ~9 doublings and a full rehash at
 *      each. The old mirror pre-sized to a power of two >= 2*N and never grew
 *      or rehashed once — it skipped that work entirely while its comment
 *      claimed to sit at "the working point kara's Map[K, V] sits at".
 *   3. Reset by CONSTRUCTION, not by memset. The old mirror cleared a 16 KiB
 *      `used` array with one memset per call.
 *
 * The hash is kāra's: for a primitive key of <= 8 bytes, `emit_hash_fn_for_type`
 * takes an inline fast path of one zext plus one multiply by the FxHash seed
 * (`src/codegen/synth.rs`), which is what `fxhash_i64` below is. The old mirror
 * used a splitmix mix — decent dispersion, but a different number of multiplies,
 * so it was also off the equal-hash axis BENCHMARKS.md tracks.
 *
 * Still open addressing with linear probing, matching kāra. No deletes, so no
 * tombstone bookkeeping is needed here.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define N 5000
#define INITIAL_CAPACITY 16   /* == runtime/src/map.rs INITIAL_CAPACITY */

/* kāra's FxHash seed (src/codegen/synth.rs FXHASH_SEED). The <=8-byte
 * primitive-key fast path is exactly one multiply by it. */
#define FXHASH_SEED 0x517cc1b727220a95ULL

static inline uint64_t fxhash_i64(int64_t k) {
    return (uint64_t)k * FXHASH_SEED;
}

typedef struct {
    int64_t *keys;
    int64_t *vals;
    bool    *used;
    size_t   capacity;   /* always a power of two */
    size_t   len;
} Map;

static void map_init(Map *m) {
    m->capacity = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = malloc(m->capacity * sizeof *m->keys);
    m->vals = malloc(m->capacity * sizeof *m->vals);
    m->used = calloc(m->capacity, sizeof *m->used);
    if (!m->keys || !m->vals || !m->used) { abort(); }
}

static void map_free(Map *m) {
    free(m->keys); free(m->vals); free(m->used);
    m->keys = NULL; m->vals = NULL; m->used = NULL;
}

/* Insert into a table known to have room and no equal key — the rehash helper. */
static void map_put_fresh(Map *m, int64_t k, int64_t v) {
    size_t mask = m->capacity - 1;
    size_t h = (size_t)(fxhash_i64(k) & mask);
    while (m->used[h]) { h = (h + 1) & mask; }
    m->used[h] = true; m->keys[h] = k; m->vals[h] = v;
}

static void map_resize(Map *m) {
    size_t old_cap = m->capacity;
    int64_t *ok = m->keys, *ov = m->vals; bool *ou = m->used;
    m->capacity = old_cap * 2;
    m->keys = malloc(m->capacity * sizeof *m->keys);
    m->vals = malloc(m->capacity * sizeof *m->vals);
    m->used = calloc(m->capacity, sizeof *m->used);
    if (!m->keys || !m->vals || !m->used) { abort(); }
    for (size_t i = 0; i < old_cap; i++) {
        if (ou[i]) { map_put_fresh(m, ok[i], ov[i]); }
    }
    free(ok); free(ov); free(ou);
}

static bool map_get(const Map *m, int64_t k, int64_t *out) {
    size_t mask = m->capacity - 1;
    size_t h = (size_t)(fxhash_i64(k) & mask);
    while (m->used[h]) {
        if (m->keys[h] == k) { *out = m->vals[h]; return true; }
        h = (h + 1) & mask;
    }
    return false;
}

static void map_insert(Map *m, int64_t k, int64_t v) {
    /* Same 75%-load trigger as runtime/src/map.rs (no tombstones here). */
    if ((m->len + 1) * 4 > m->capacity * 3) { map_resize(m); }
    size_t mask = m->capacity - 1;
    size_t h = (size_t)(fxhash_i64(k) & mask);
    while (m->used[h]) {
        if (m->keys[h] == k) { m->vals[h] = v; return; }
        h = (h + 1) & mask;
    }
    m->used[h] = true; m->keys[h] = k; m->vals[h] = v;
    m->len++;
}

static int two_sum(const int64_t *nums, int64_t target, size_t *oi, size_t *oj) {
    Map seen;
    map_init(&seen);                 /* fresh map per call, as the kara source does */
    for (size_t i = 0; i < N; i++) {
        int64_t complement = target - nums[i];
        int64_t j;
        if (map_get(&seen, complement, &j)) {
            *oi = (size_t)j;
            *oj = i;
            map_free(&seen);
            return 1;
        }
        map_insert(&seen, nums[i], (int64_t)i);
    }
    map_free(&seen);
    return 0;
}

int main(void) {
    int64_t data[N];
    for (size_t i = 0; i < N; i++) {
        data[i] = ((int64_t)i * 7) % 1000;
    }

    const int64_t target = -1;
    int64_t sum = 0;
    for (int k = 0; k < 10; k++) {
        size_t i, j;
        if (two_sum(data, target, &i, &j)) {
            sum += (int64_t)i + (int64_t)j;
        } else {
            sum += -2;
        }
    }
    printf("%lld\n", (long long)sum);
    return 0;
}

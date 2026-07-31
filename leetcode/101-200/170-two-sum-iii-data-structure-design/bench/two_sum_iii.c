#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload — Two Sum III, LeetCode #170.
 *
 * Algorithmic mirror of two_sum_iii.kara: same LCG, same N_ADD / M_QUERY,
 * same add/find, same sink.
 *
 * C has no stdlib hash map, so `counts` is a hand-rolled open-addressing table
 * shaped to match the runtime's Map[i64, i64]:
 *
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * Two earlier parity breaks, both now fixed:
 *
 *   1. `counts` was a direct-address table over [0, K) — an array indexed by
 *      the key, with no hash and no probe. Every other mirror hashes. That is
 *      not a fast C map, it is a different data structure.
 *   2. `find` scanned every key and OR-ed the results, while the kata returns
 *      as soon as a pair is found. Scanning all keys is strictly more work, so
 *      it penalized the mirrors rather than the kata. Now all four return
 *      early. The amount of work this skips depends on hash iteration order,
 *      which genuinely differs per language — over 1.2M queries that averages
 *      out, but it is a real source of cross-language variance and is the
 *      price of matching the kata's control flow. */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long long *keys;
    long long *vals;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static inline unsigned long long fxhash_i64(long long k) {
    return (unsigned long long)k * FXHASH_SEED;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = (long long *)malloc(m->cap * sizeof(long long));
    m->vals = (long long *)malloc(m->cap * sizeof(long long));
    m->used = (unsigned char *)calloc(m->cap, 1);
}

/* Insert without the load check or the duplicate check — callers guarantee both. */
static void map_put_fresh(Map *m, long long k, long long v) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (m->used[h]) {
        h = (h + 1) & mask;
    }
    m->used[h] = 1;
    m->keys[h] = k;
    m->vals[h] = v;
    m->len++;
}

static void map_grow(Map *m) {
    long long *ok = m->keys;
    long long *ov = m->vals;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->len = 0;
    m->keys = (long long *)malloc(m->cap * sizeof(long long));
    m->vals = (long long *)malloc(m->cap * sizeof(long long));
    m->used = (unsigned char *)calloc(m->cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            map_put_fresh(m, ok[i], ov[i]);
        }
    }
    free(ok);
    free(ov);
    free(ou);
}

/* Returns a pointer to the stored value, or NULL if the key is absent. */
static long long *map_get(const Map *m, long long k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (m->used[h]) {
        if (m->keys[h] == k) {
            return (long long *)&m->vals[h];
        }
        h = (h + 1) & mask;
    }
    return NULL;
}

static void map_insert(Map *m, long long k, long long v) {
    long long *slot = map_get(m, k);
    if (slot) {
        *slot = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
    }
    map_put_fresh(m, k, v);
}

typedef struct {
    Map counts;
} TwoSum;

static void new_two_sum(TwoSum *ds) { map_init(&ds->counts); }

static void add(TwoSum *ds, long long number) {
    long long *c = map_get(&ds->counts, number);
    map_insert(&ds->counts, number, c ? *c + 1 : 1);
}

static int find(const TwoSum *ds, long long value) {
    const Map *m = &ds->counts;
    for (size_t i = 0; i < m->cap; i++) {
        if (!m->used[i]) {
            continue;
        }
        long long k = m->keys[i];
        long long complement = value - k;
        if (complement == k) {
            long long *c = map_get(m, k);
            if (c && *c >= 2) {
                return 1;
            }
        } else {
            if (map_get(m, complement)) {
                return 1;
            }
        }
    }
    return 0;
}

int main(void) {
    long k_range = 6000;
    long n_add = 170, m_query = 1200000;

    TwoSum ds;
    new_two_sum(&ds);

    long state = 12345;
    for (long i = 0; i < n_add; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        add(&ds, state % k_range);
    }

    long sink = 0;
    for (long q = 0; q < m_query; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long target = state % (2 * k_range);
        if (find(&ds, target)) sink++;
    }
    printf("%ld\n", sink);
    return 0;
}

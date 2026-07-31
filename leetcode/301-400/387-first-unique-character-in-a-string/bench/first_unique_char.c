/* Benchmark harness for LeetCode #387 — Map (general-alphabet) approach.
 * Mirrors first_unique_char.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so one is hand-rolled here: open addressing with
 * linear probing, same insert/get/key-walk semantics as the Kara/Rust/Go/Python
 * maps. Deliberately NOT a direct-address count table — a direct-address table
 * would be a different algorithm and would flatter C in the comparison.
 *
 * The table is shaped to match the runtime's Map[K,V] rather than presized to
 * the workload:
 *
 *   - heap-allocated per call, like the kata's `Map.new()`, and freed on the
 *     way out;
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * This matters here: the working set is 26 keys, so the previous fixed
 * 64-entry stack table sat at 41% load and never allocated, grew, or rehashed,
 * while the kata's map allocates and rehashes 16 -> 32 -> 64 on each of the
 * 8000 calls. Presizing to the answer is not a C advantage, it is a different
 * program.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long long *key;
    long long *val;
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
    m->key = (long long *)malloc(m->cap * sizeof(long long));
    m->val = (long long *)malloc(m->cap * sizeof(long long));
    m->used = (unsigned char *)calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->key);
    free(m->val);
    free(m->used);
}

static size_t map_slot(const Map *m, long long k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (m->used[h] && m->key[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static long long map_get(const Map *m, long long k, long long dflt) {
    size_t h = map_slot(m, k);
    return m->used[h] ? m->val[h] : dflt;
}

static void map_grow(Map *m) {
    long long *ok = m->key;
    long long *ov = m->val;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->key = (long long *)malloc(m->cap * sizeof(long long));
    m->val = (long long *)malloc(m->cap * sizeof(long long));
    m->used = (unsigned char *)calloc(m->cap, 1);

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

static void map_insert(Map *m, long long k, long long v) {
    size_t h = map_slot(m, k);
    if (m->used[h]) {
        m->val[h] = v;
        return;
    }
    /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
    if ((m->len + 1) * 4 > m->cap * 3) {
        map_grow(m);
        h = map_slot(m, k);
    }
    m->used[h] = 1;
    m->key[h] = k;
    m->val[h] = v;
    m->len++;
}

static long long first_uniq_char(const long long *bs, long long len) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long c = bs[i];
        map_insert(&counts, c, map_get(&counts, c, 0) + 1);
    }

    long long res = -1;
    for (long long j = 0; j < len; j++) {
        if (map_get(&counts, bs[j], 0) == 1) {
            res = j;
            break;
        }
    }
    map_free(&counts);
    return res;
}

static long long unique_count(const long long *bs, long long len) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long c = bs[i];
        map_insert(&counts, c, map_get(&counts, c, 0) + 1);
    }
    long long uniq = 0;
    for (size_t h = 0; h < counts.cap; h++) { /* the keys() walk */
        if (counts.used[h] && map_get(&counts, counts.key[h], 0) == 1) {
            uniq++;
        }
    }
    map_free(&counts);
    return uniq;
}

#define N 4000
#define ITERS 2000

int main(void) {
    static long long bs[N];
    for (long long i = 0; i < N; i++) {
        bs[i] = 97 + (i % 25);
    }
    bs[N - 1] = 122;

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long p = (it * 7919) % N;
        bs[p] = 97 + (it % 25);
        sink += first_uniq_char(bs, N);
        sink += unique_count(bs, N);
    }
    printf("%lld\n", sink);
    return 0;
}

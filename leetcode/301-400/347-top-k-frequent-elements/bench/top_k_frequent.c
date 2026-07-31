/* Benchmark harness for LeetCode #347 — scalar-keyed Map approach.
 * Mirrors top_k_frequent.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so one is hand-rolled: open addressing with linear
 * probing, same insert/get/key-walk semantics as the Kara/Rust/Go/Python maps.
 * Deliberately NOT a direct-address count table — that would be a different
 * algorithm and would flatter C in the comparison.
 *
 * The sort key is a total order (count desc, then key asc, keys distinct), so
 * the sorted result is unique regardless of the map's iteration order. That is
 * what makes the sink comparable across five different map implementations.
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
 * The previous fixed 512-entry stack table was presized to just past the
 * 200-key working set, so it never allocated, grew, or rehashed, while the
 * kata's map climbs 16 -> 32 -> ... -> 512 on each of the 300 calls. Presizing
 * to the answer is not a C advantage, it is a different program.
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

#define N 8000
#define D 200
#define ITERS 300
#define K 10

static long long top_k_sum(const long long *nums, long long len, long long k) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long v = nums[i];
        map_insert(&counts, v, map_get(&counts, v, 0) + 1);
    }

    long long *vals = (long long *)malloc(counts.len * sizeof(long long));
    long long nvals = 0;
    for (size_t h = 0; h < counts.cap; h++) { /* the keys() walk */
        if (counts.used[h]) {
            vals[nvals++] = counts.key[h];
        }
    }

    for (long long a = 1; a < nvals; a++) {
        long long cur = vals[a];
        long long cur_c = map_get(&counts, cur, 0);
        long long b = a - 1;
        while (b >= 0) {
            long long prev = vals[b];
            long long prev_c = map_get(&counts, prev, 0);
            int shift = 0;
            if (prev_c < cur_c) {
                shift = 1;
            }
            if (prev_c == cur_c && prev > cur) {
                shift = 1;
            }
            if (!shift) {
                break;
            }
            vals[b + 1] = prev;
            b--;
        }
        vals[b + 1] = cur;
    }

    long long limit = k < nvals ? k : nvals;
    long long sum = 0;
    for (long long t = 0; t < limit; t++) {
        sum += vals[t];
    }
    free(vals);
    map_free(&counts);
    return sum;
}

int main(void) {
    static long long bs[N];
    for (long long i = 0; i < N; i++) {
        long long v = i % D;
        if (i % 5 == 0) {
            v = i % 13;
        }
        bs[i] = v;
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long p = (it * 7919) % N;
        bs[p] = (it * 37) % D;
        sink += top_k_sum(bs, N, K);
    }
    printf("%lld\n", sink);
    return 0;
}

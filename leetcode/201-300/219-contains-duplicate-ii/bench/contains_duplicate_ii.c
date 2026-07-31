#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #219 — Contains Duplicate II.
 *
 * The kata's kernel is a value->last-index hash map: as it scans, a value whose
 * previous index is within window k is a "nearby duplicate". One boolean query
 * short-circuits on the first hit, so it cannot sustain a benchmark. The bench
 * keeps the identical map kernel but runs it as a full sweep that COUNTS nearby
 * duplicates, over every window width k in 1..KMAX, on ONE big PRNG array. Every
 * k forces a full value->index scan (real map throughput, no early-exit erosion);
 * the per-element get+insert with a data-dependent gap branch does not vectorize.
 * Sink = total nearby-duplicate hits summed over all k. (Same scaling spirit as
 * #216 counting combinations instead of listing them.)
 *
 * C mirrors the language maps with an open-addressing table shaped to match the
 * runtime's Map[K,V] rather than presized to the workload:
 *
 *   - heap-allocated per k, like the kata's `Map.new()`, and freed after;
 *   - capacity 16 initially, power of two, linear probing;
 *   - grow (double + full rehash) when (len + 1) * 4 > capacity * 3, i.e. the
 *     same 75% load factor as the runtime map;
 *   - FxHash on the key with the same seed the compiler synthesizes (for a
 *     <= 8-byte primitive key that is a single zext + multiply).
 *
 * The previous version was a fixed 131 072-entry static table with a per-run
 * generation stamp for an O(1) logical clear. The stamp itself is a fair trick
 * (it avoids a memset that would distort the measured churn), but the table
 * was presized past the 49 999-value range, so it never allocated, grew, or
 * rehashed -- while the kata's map climbs 16 -> 32 -> ... -> 131 072, thirteen
 * doublings and thirteen full rehashes, on each of the 40 sweeps. Presizing to
 * the answer is not a C advantage, it is a different program. */

#define N      1000000L    /* array length                          */
#define KMAX   40L         /* sweep k = 1..KMAX                      */
#define M      49999L      /* value range (0..M-1); prime, breaks LCG lattice */

#define INITIAL_CAPACITY 16UL
#define FXHASH_SEED 0x517cc1b727220a95ULL

typedef struct {
    long *keys;
    long *idxs;
    unsigned char *used;
    size_t cap;
    size_t len;
} Map;

static inline unsigned long fxhash_i64(long k) {
    return (unsigned long)k * FXHASH_SEED;
}

static void map_init(Map *m) {
    m->cap = INITIAL_CAPACITY;
    m->len = 0;
    m->keys = malloc(m->cap * sizeof(long));
    m->idxs = malloc(m->cap * sizeof(long));
    m->used = calloc(m->cap, 1);
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->idxs);
    free(m->used);
}

static size_t map_slot(const Map *m, long k) {
    size_t mask = m->cap - 1;
    size_t h = (size_t)fxhash_i64(k) & mask;
    while (m->used[h] && m->keys[h] != k) {
        h = (h + 1) & mask;
    }
    return h;
}

static void map_grow(Map *m) {
    long *ok = m->keys;
    long *oi = m->idxs;
    unsigned char *ou = m->used;
    size_t ocap = m->cap;

    m->cap = ocap * 2;
    m->keys = malloc(m->cap * sizeof(long));
    m->idxs = malloc(m->cap * sizeof(long));
    m->used = calloc(m->cap, 1);

    for (size_t i = 0; i < ocap; i++) {
        if (ou[i]) {
            size_t h = map_slot(m, ok[i]);
            m->used[h] = 1;
            m->keys[h] = ok[i];
            m->idxs[h] = oi[i];
        }
    }
    free(ok);
    free(oi);
    free(ou);
}

static long count_nearby(const long *a, long k) {
    Map m;
    map_init(&m);
    long hits = 0;
    for (long i = 0; i < N; i++) {
        long x = a[i];
        size_t h = map_slot(&m, x);
        if (m.used[h]) {
            if (i - m.idxs[h] <= k) hits += 1;
            m.idxs[h] = i; /* keep only the latest index */
            continue;
        }
        /* runtime map: resize when (len + tombstones + 1) * 4 > capacity * 3 */
        if ((m.len + 1) * 4 > m.cap * 3) {
            map_grow(&m);
            h = map_slot(&m, x);
        }
        m.used[h] = 1;
        m.keys[h] = x;
        m.idxs[h] = i;
        m.len++;
    }
    map_free(&m);
    return hits;
}

int main(void) {
    long *a = malloc(N * sizeof(long));
    long state = 12345;
    for (long i = 0; i < N; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        a[i] = state % M;
    }

    long sink = 0;
    for (long k = 1; k <= KMAX; k++) {
        sink += count_nearby(a, k);
    }
    printf("%ld\n", sink);
    free(a);
    return 0;
}

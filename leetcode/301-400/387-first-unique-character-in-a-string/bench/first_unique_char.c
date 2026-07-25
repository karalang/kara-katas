/* Benchmark harness for LeetCode #387 — Map (general-alphabet) approach.
 * Mirrors first_unique_char.kara algorithm-for-algorithm.
 *
 * C has no stdlib hash map, so one is hand-rolled here: open addressing with
 * linear probing, same insert/get/key-walk semantics as the Kara/Rust/Go/Python
 * maps. Deliberately NOT a direct-address count table — a direct-address table
 * would be a different algorithm and would flatter C in the comparison.
 */

#include <stdio.h>
#include <string.h>

#define MAPCAP 64 /* power of two; >= 2x the 26-key working set */

typedef struct {
    long long key[MAPCAP];
    long long val[MAPCAP];
    unsigned char used[MAPCAP];
} Map;

static void map_init(Map *m) { memset(m->used, 0, sizeof(m->used)); }

static size_t map_slot(const Map *m, long long k) {
    size_t h = (size_t)((unsigned long long)k * 1099511628211ULL) & (MAPCAP - 1);
    while (m->used[h] && m->key[h] != k) {
        h = (h + 1) & (MAPCAP - 1);
    }
    return h;
}

static long long map_get(const Map *m, long long k, long long dflt) {
    size_t h = map_slot(m, k);
    return m->used[h] ? m->val[h] : dflt;
}

static void map_insert(Map *m, long long k, long long v) {
    size_t h = map_slot(m, k);
    m->used[h] = 1;
    m->key[h] = k;
    m->val[h] = v;
}

static long long first_uniq_char(const long long *bs, long long len) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long c = bs[i];
        map_insert(&counts, c, map_get(&counts, c, 0) + 1);
    }

    for (long long j = 0; j < len; j++) {
        if (map_get(&counts, bs[j], 0) == 1) {
            return j;
        }
    }
    return -1;
}

static long long unique_count(const long long *bs, long long len) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long c = bs[i];
        map_insert(&counts, c, map_get(&counts, c, 0) + 1);
    }
    long long uniq = 0;
    for (size_t h = 0; h < MAPCAP; h++) { /* the keys() walk */
        if (counts.used[h] && map_get(&counts, counts.key[h], 0) == 1) {
            uniq++;
        }
    }
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

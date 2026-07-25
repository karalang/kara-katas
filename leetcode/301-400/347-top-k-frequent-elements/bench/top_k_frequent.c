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
 */

#include <stdio.h>
#include <string.h>

#define MAPCAP 512 /* power of two; >= 2x the 200-key working set */

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

#define N 8000
#define D 200
#define ITERS 300
#define K 10

static long long vals[MAPCAP];

static long long top_k_sum(const long long *nums, long long len, long long k) {
    Map counts;
    map_init(&counts);
    for (long long i = 0; i < len; i++) {
        long long v = nums[i];
        map_insert(&counts, v, map_get(&counts, v, 0) + 1);
    }

    long long nvals = 0;
    for (size_t h = 0; h < MAPCAP; h++) { /* the keys() walk */
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

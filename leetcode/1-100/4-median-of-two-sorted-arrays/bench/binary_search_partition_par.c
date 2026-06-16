/* LeetCode #4 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * binary_search_partition).
 * Same middle_pair_off binary-search-partition; the K=10M reduction split
 * across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is measured
 * against. Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 binary_search_partition_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define M 1000000LL
#define N 1000000LL
#define R 1000LL
#define K_ITERS 10000000LL

typedef struct { int64_t lower, upper; } Pair;

static inline int64_t i64_min(int64_t a, int64_t b) { return a < b ? a : b; }
static inline int64_t i64_max(int64_t a, int64_t b) { return a > b ? a : b; }

static Pair middle_pair_off(const int64_t *a, int64_t a_off, int64_t a_len,
                            const int64_t *b, int64_t b_off, int64_t b_len) {
    if (a_len > b_len) {
        return middle_pair_off(b, b_off, b_len, a, a_off, a_len);
    }
    int64_t half = (a_len + b_len + 1) / 2;
    int64_t lo = 0, hi = a_len;
    while (lo <= hi) {
        int64_t i = (lo + hi) / 2;
        int64_t j = half - i;
        int64_t left_a  = (i > 0)     ? a[a_off + i - 1] : INT64_MIN;
        int64_t right_a = (i < a_len) ? a[a_off + i]     : INT64_MAX;
        int64_t left_b  = (j > 0)     ? b[b_off + j - 1] : INT64_MIN;
        int64_t right_b = (j < b_len) ? b[b_off + j]     : INT64_MAX;
        if (left_a > right_b) {
            hi = i - 1;
        } else if (left_b > right_a) {
            lo = i + 1;
        } else {
            int64_t lower = i64_max(left_a, left_b);
            if ((a_len + b_len) % 2 == 1) {
                return (Pair){lower, lower};
            }
            int64_t upper = i64_min(right_a, right_b);
            return (Pair){lower, upper};
        }
    }
    __builtin_unreachable();
}

typedef struct {
    const int64_t *base_a;
    const int64_t *base_b;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t off = k % R;
        Pair p = middle_pair_off(wk->base_a, off, M, wk->base_b, off, N);
        s += p.lower + p.upper;
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    int64_t *base_a = (int64_t *)malloc(sizeof(int64_t) * (size_t)(M + R));
    int64_t *base_b = (int64_t *)malloc(sizeof(int64_t) * (size_t)(N + R));
    for (int64_t p = 0; p < M + R; p++) base_a[p] = 2 * p;
    for (int64_t p = 0; p < N + R; p++) base_b[p] = 2 * p + 1;

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].base_a = base_a;
        works[w].base_b = base_b;
        works[w].start = (int64_t)w * chunk;
        works[w].end = (w == nworkers - 1) ? K_ITERS : ((int64_t)w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    free(base_a);
    free(base_b);
    return 0;
}

/* LeetCode #153 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, binary_search).
 * Same O(log n) find_min; the K=2_000_000-call reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS threads,
 * no runtime — the ceiling auto-par is measured against. Sink = 2000000 (K × min 1).
 * Build: clang -O3 binary_search_par.c -o … -lpthread */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define N 2000000
#define R 666666
#define K 2000000

/* Mirrors the seq lane's black_box_slice — stops -O3 hoisting the loop-invariant
 * pure find_min out of the per-worker K-loop (2M calls → 1). */
static const int64_t *black_box_slice(const int64_t *p) {
#if defined(__GNUC__) || defined(__clang__)
    __asm__ volatile("" : "+r"(p) :: "memory");
#endif
    return p;
}

static int64_t find_min(const int64_t *nums, size_t len) {
    size_t lo = 0;
    size_t hi = len - 1;
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return nums[lo];
}

typedef struct {
    const int64_t *data;
    long start, end;
    int64_t partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (long it = w->start; it < w->end; it++) {
        s += find_min(black_box_slice(w->data), (size_t)N);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    int64_t *data = (int64_t *)malloc((size_t)N * sizeof(int64_t));
    for (size_t i = 0; i < (size_t)N; i++) {
        data[i] = (int64_t)(((i + R) % N) + 1);
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    if (nworkers > K) {
        nworkers = K;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = K / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].data = data;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? K : (w + 1) * chunk;
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
    free(data);
    return 0;
}

/* LeetCode #11 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, container).
 * Same two-pointer max_area_off; the K=10M reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 container_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define N 8
#define W 16
#define TOTAL (N * W)
#define K_ITERS 10000000LL

static int64_t max_area_off(const int64_t *heights, int64_t lo, int64_t hi) {
    int64_t l = lo;
    int64_t r = hi;
    int64_t best = 0;
    while (l < r) {
        int64_t h_l = heights[l];
        int64_t h_r = heights[r];
        int64_t h = h_l < h_r ? h_l : h_r;
        int64_t area = h * (r - l);
        if (area > best) {
            best = area;
        }
        if (h_l < h_r) {
            l += 1;
        } else {
            r -= 1;
        }
    }
    return best;
}

typedef struct {
    const int64_t *heights;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % N;
        int64_t lo = idx * W;
        int64_t hi = lo + W - 1;
        s += max_area_off(wk->heights, lo, hi);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    int64_t *heights = (int64_t *)calloc((size_t)TOTAL, sizeof(int64_t));
    for (int64_t i = 0; i < TOTAL; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        int64_t v = ((raw % 50) + 50) % 50;
        heights[i] = v;
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].heights = heights;
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
    free(heights);
    return 0;
}

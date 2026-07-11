/*
 * LeetCode #75 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 * Same batch of K=2000 independent Dutch National Flag sorts as sort_colors.c;
 * the associative sum reduction is split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk the seed range, join+merge).
 * Raw OS threads, no runtime — the ceiling Kara's auto-par is measured against.
 * Each call grows its own realloc-doubling buffer (matching Kara's Vec). Sink
 * matches the seq mirrors. Build: clang -O3 sort_colors_par.c -o … -lpthread
 */
#include <pthread.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#define N 59999
#define ITERS 2000

static int64_t sort_and_hash(int64_t seed) {
    int64_t *a = NULL;
    int64_t len = 0, cap = 0;
    for (int64_t j = 0; j < N; j++) {
        if (len == cap) {
            cap = cap ? cap * 2 : 1;
            a = (int64_t *)realloc(a, sizeof(int64_t) * (size_t)cap);
        }
        a[len++] = (j * 7 + seed) % 3;
    }
    int64_t low = 0, mid = 0, high = N - 1;
    while (mid <= high) {
        if (a[mid] == 0) {
            int64_t t = a[low]; a[low] = a[mid]; a[mid] = t;
            low++; mid++;
        } else if (a[mid] == 1) {
            mid++;
        } else {
            int64_t t = a[mid]; a[mid] = a[high]; a[high] = t;
            high--;
        }
    }
    int64_t acc = 0;
    for (int64_t j = 0; j < N; j++)
        acc = (acc * 131 + a[j]) % 1000000007;
    free(a);
    return acc;
}

typedef struct { int64_t start, end, partial; } Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (int64_t i = w->start; i < w->end; i++)
        s += sort_and_hash(i);
    w->partial = s;
    return NULL;
}

int main(void) {
    int64_t nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) nworkers = 1;
    if (nworkers > ITERS) nworkers = ITERS;

    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = ITERS / nworkers;
    for (int64_t w = 0; w < nworkers; w++) {
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (int64_t w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    return 0;
}

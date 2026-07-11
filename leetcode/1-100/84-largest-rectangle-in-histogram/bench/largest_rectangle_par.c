/*
 * LeetCode #84 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 * Same batch of K=108000 independent largest-rectangle computations as
 * largest_rectangle.c; the associative sum reduction is split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk the seed range, join + merge). Raw
 * OS threads, no runtime — the ceiling Kara's auto-par is measured against. Sink
 * matches the seq mirrors. Build: clang -O3 largest_rectangle_par.c -o … -lpthread
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define N 2000
#define ITERS 108000

static int64_t largest_rectangle(const int64_t *heights, int64_t n) {
    int64_t *stack = (int64_t *)malloc((n + 1) * sizeof(int64_t));
    int64_t sp = 0;
    int64_t max_area = 0;
    for (int64_t i = 0; i <= n; i++) {
        int64_t h = (i < n) ? heights[i] : 0;
        while (sp > 0 && heights[stack[sp - 1]] > h) {
            int64_t top = stack[--sp];
            int64_t height = heights[top];
            int64_t width = (sp == 0) ? i : (i - stack[sp - 1] - 1);
            int64_t area = height * width;
            if (area > max_area) max_area = area;
        }
        stack[sp++] = i;
    }
    free(stack);
    return max_area;
}

static int64_t compute(int64_t seed) {
    int64_t *h = (int64_t *)malloc(N * sizeof(int64_t));
    for (int64_t j = 0; j < N; j++)
        h[j] = (j + seed) % 50;
    int64_t area = largest_rectangle(h, N);
    free(h);
    return area;
}

typedef struct { int64_t start, end, partial; } Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (int64_t i = w->start; i < w->end; i++)
        s += compute(i);
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

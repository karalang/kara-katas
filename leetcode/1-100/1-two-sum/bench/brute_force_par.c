/* LeetCode #1 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, brute_force).
 * Same O(n²) two_sum; the 100-call reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS threads,
 * no runtime — the ceiling auto-par is measured against. Sink = -200.
 * Build: clang -O3 brute_force_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define N 5000
#define ITERS 100

static long two_sum_result(const long *nums, long target) {
    for (long i = 0; i < N; i++) {
        for (long j = i + 1; j < N; j++) {
            if (nums[i] + nums[j] == target) {
                return i + j;
            }
        }
    }
    return -2;
}

typedef struct {
    const long *data;
    long target, start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long s = 0;
    for (long k = w->start; k < w->end; k++) {
        s += two_sum_result(w->data, w->target);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    long *data = malloc((size_t)N * sizeof(long));
    for (long i = 0; i < N; i++) {
        data[i] = (i * 7) % 1000;
    }
    long target = -1;

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    if (nworkers > ITERS) {
        nworkers = ITERS;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].data = data;
        works[w].target = target;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    long total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%ld\n", total);
    free(threads);
    free(works);
    free(data);
    return 0;
}

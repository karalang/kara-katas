/* LeetCode #28 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, brute_force).
 * Same brute-force sliding-window str_str; the K-call reduction split across a
 * fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge).
 * Raw OS threads, no runtime — the ceiling auto-par is measured against.
 * Sink = 199998400 (K=100 × first-match index 1999984).
 * Build: clang -O3 brute_force_par.c -o … -lpthread */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define N 2000000
#define M 16
#define ITERS 100

static int64_t str_str(const uint8_t *haystack, int64_t hn, const uint8_t *needle,
                       int64_t nn) {
    if (nn == 0) {
        return 0;
    }
    if (nn > hn) {
        return -1;
    }
    for (int64_t i = 0; i <= hn - nn; i++) {
        int64_t j = 0;
        while (j < nn && haystack[i + j] == needle[j]) {
            j++;
        }
        if (j == nn) {
            return i;
        }
    }
    return -1;
}

typedef struct {
    const uint8_t *haystack, *needle;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = w->start; k < w->end; k++) {
        s += str_str(w->haystack, (int64_t)N, w->needle, (int64_t)M);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    uint8_t *haystack = (uint8_t *)malloc(N);
    for (int64_t i = 0; i < N; i++) {
        haystack[i] = 'a';
    }
    haystack[N - 1] = 'b';
    uint8_t *needle = (uint8_t *)malloc(M);
    for (int64_t i = 0; i < M; i++) {
        needle[i] = 'a';
    }
    needle[M - 1] = 'b';

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    if (nworkers > ITERS) {
        nworkers = ITERS;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].haystack = haystack;
        works[w].needle = needle;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
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
    free(haystack);
    free(needle);
    return 0;
}

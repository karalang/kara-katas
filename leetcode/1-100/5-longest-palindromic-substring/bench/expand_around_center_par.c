/* LeetCode #5 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, expand_around_center).
 * Same O(n²) expand-around-center longest_palindrome; the K=100-call reduction
 * split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is measured
 * against. Sink = 500000 (K=100 × (best_start 0 + best_len 5000)).
 * Build: clang -O3 expand_around_center_par.c -o … -lpthread */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define N 5000
#define ITERS 100

static void expand(const char *s, int64_t n, int64_t lo0, int64_t hi0,
                   int64_t *out_lo, int64_t *out_len) {
    int64_t lo = lo0;
    int64_t hi = hi0;
    while (lo >= 0 && hi < n && s[lo] == s[hi]) {
        lo--;
        hi++;
    }
    *out_lo = lo + 1;
    *out_len = hi - lo - 1;
}

static void longest_palindrome(const char *s, int64_t n, int64_t *best_start,
                               int64_t *best_len) {
    int64_t bs = 0;
    int64_t bl = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t start, length;
        expand(s, n, i, i, &start, &length);
        if (length > bl) {
            bs = start;
            bl = length;
        }
        expand(s, n, i, i + 1, &start, &length);
        if (length > bl) {
            bs = start;
            bl = length;
        }
    }
    *best_start = bs;
    *best_len = bl;
}

typedef struct {
    const char *data;
    long start, end;
    int64_t partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (long k = w->start; k < w->end; k++) {
        int64_t bs, bl;
        longest_palindrome(w->data, (int64_t)N, &bs, &bl);
        s += bs + bl;
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    char *data = (char *)malloc((size_t)N + 1);
    memset(data, 'a', (size_t)N);
    data[N] = '\0';

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
    free(data);
    return 0;
}

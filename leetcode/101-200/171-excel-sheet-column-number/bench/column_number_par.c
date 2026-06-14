/* LeetCode #171 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 *
 * Same Horner-fold base-26 parse as column_number.c, but the K_ITERS reduction
 * is split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (each worker
 * runs a contiguous k-range, replicating the `k % LEN` round-robin into a
 * private partial, then join+merge). The corpus is built once, shared read-only.
 * The ceiling, not a competitor: raw OS threads with zero runtime/GC overhead —
 * how much parallel throughput Kara's auto-par (zero parallel source) leaves on
 * the table vs metal. Same sink as every mirror.
 *
 * Build: clang -O3 column_number_par.c -o … -lpthread
 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define LEN 50000L
#define K_ITERS 100000000L

static const char LETTERS[26] = {
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};

static char *to_title(long num) {
    char tmp[16];
    int len = 0;
    while (num > 0) {
        num -= 1;
        tmp[len++] = LETTERS[num % 26];
        num /= 26;
    }
    char *out = malloc((size_t)len + 1);
    for (int i = 0; i < len; i++) {
        out[i] = tmp[len - 1 - i];
    }
    out[len] = '\0';
    return out;
}

static long to_number(const char *title) {
    long n = 0;
    for (const char *p = title; *p; p++) {
        n = n * 26 + (long)(*p - 'A') + 1;
    }
    return n;
}

typedef struct {
    char **corpus;
    long start, end;
    long partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long s = 0;
    for (long k = w->start; k < w->end; k++) {
        s += to_number(w->corpus[k % LEN]);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    char **corpus = malloc((size_t)LEN * sizeof(char *));
    for (long i = 0; i < LEN; i++) {
        corpus[i] = to_title(i + 1);
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = K_ITERS / nworkers;

    for (long w = 0; w < nworkers; w++) {
        works[w].corpus = corpus;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? K_ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }

    long total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }

    printf("%ld\n", total);
    for (long i = 0; i < LEN; i++) {
        free(corpus[i]);
    }
    free(corpus);
    free(threads);
    free(works);
    return 0;
}

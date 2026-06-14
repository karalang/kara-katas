/* LeetCode #204 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 *
 * Same trial-division primality test as count.c, but the [0, N) range is split
 * across a fixed pool of _SC_NPROCESSORS_ONLN pthreads — each worker collects
 * the primes in its chunk into a private buffer (matching the seq mirror's and
 * go-par's collect-then-sum work, so the comparison stays apples-to-apples),
 * then a join + merge + sum. The bare-metal FLOOR (raw OS threads, no runtime /
 * work-stealing / GC): how much auto-par leaves on the table vs metal, and the
 * most parallel boilerplate of any mirror, against Kara's zero. Same (count,
 * sum) sink as every other mirror.
 *
 * Build: clang -O3 count_par.c -o ... -lpthread
 */
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define N 10000000

static bool is_prime(int64_t n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if ((n % 2) == 0) return false;
    for (int64_t i = 3; i * i <= n; i += 2) {
        if ((n % i) == 0) return false;
    }
    return true;
}

typedef struct {
    int64_t start, end;
    int64_t *buf;
    size_t len;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    size_t cap = 65536;
    w->buf = malloc(cap * sizeof(int64_t));
    w->len = 0;
    for (int64_t k = w->start; k < w->end; k++) {
        if (is_prime(k)) {
            if (w->len >= cap) {
                cap *= 2;
                w->buf = realloc(w->buf, cap * sizeof(int64_t));
            }
            w->buf[w->len++] = k;
        }
    }
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = (int64_t)N / nworkers;

    for (long w = 0; w < nworkers; w++) {
        works[w].start = (int64_t)w * chunk;
        works[w].end = (w == nworkers - 1) ? (int64_t)N : (int64_t)(w + 1) * chunk;
        works[w].buf = NULL;
        works[w].len = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }

    size_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].len;
    }

    /* Merge into one contiguous buffer (matches the seq/go-par collect step),
     * then reduce. Chunks are contiguous ascending, so the merge is sorted —
     * but the (count, sum) sink is order-independent regardless. */
    int64_t *primes = malloc((total ? total : 1) * sizeof(int64_t));
    size_t off = 0;
    for (long w = 0; w < nworkers; w++) {
        memcpy(primes + off, works[w].buf, works[w].len * sizeof(int64_t));
        off += works[w].len;
        free(works[w].buf);
    }

    int64_t sum = 0;
    for (size_t i = 0; i < total; i++) {
        sum += primes[i];
    }
    printf("%zu\n", total);
    printf("%lld\n", (long long)sum);

    free(primes);
    free(threads);
    free(works);
    return 0;
}

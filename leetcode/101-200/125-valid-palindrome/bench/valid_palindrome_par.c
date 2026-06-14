/* LeetCode #125 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 *
 * Same allocating filter-then-compare as valid_palindrome.c, but the ITERS
 * reduction is split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads
 * (spawn once, each worker checks a contiguous chunk into a private partial,
 * then join+merge). The ceiling, not a competitor: raw OS threads, zero
 * runtime/work-stealing/GC — how much auto-par leaves on the table vs metal,
 * and the most parallel boilerplate of any mirror. Same sink (3000000).
 *
 * Build: clang -O3 valid_palindrome_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ITERS 3000000
#define REPEAT 8
#define BASE "A man, a plan, a canal: Panama"

static int is_alnum(unsigned char b) {
    return (b >= '0' && b <= '9') || (b >= 'a' && b <= 'z') || (b >= 'A' && b <= 'Z');
}

static int is_palindrome(const unsigned char *s, long n) {
    unsigned char *clean = malloc((size_t)(n > 0 ? n : 1));
    long m = 0;
    for (long i = 0; i < n; i++) {
        unsigned char b = s[i];
        if (is_alnum(b)) {
            clean[m++] = (b >= 'A' && b <= 'Z') ? (unsigned char)(b + 32) : b;
        }
    }
    int ok = 1;
    long lo = 0, hi = m - 1;
    while (lo < hi) {
        if (clean[lo] != clean[hi]) { ok = 0; break; }
        lo++;
        hi--;
    }
    free(clean);
    return ok;
}

typedef struct {
    const unsigned char *input;
    long n, start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long s = 0;
    for (long it = w->start; it < w->end; it++) {
        s += is_palindrome(w->input, w->n);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    long base_len = (long)strlen(BASE);
    long n = base_len * REPEAT;
    unsigned char *input = malloc((size_t)n);
    for (int r = 0; r < REPEAT; r++) {
        memcpy(input + (long)r * base_len, BASE, (size_t)base_len);
    }
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].input = input;
        works[w].n = n;
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
    free(input);
    return 0;
}

/* LeetCode #13 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, greedy).
 * Same int_to_roman / roman_to_int; the K=10M reduction split across a fixed
 * pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 -pthread greedy_par.c -o … */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define K_ITERS 10000000LL

static int int_to_roman(int64_t num, int32_t *out) {
    int len = 0;
    int64_t n = num;
    while (n >= 1000) { out[len++] = 'M'; n -= 1000; }
    if    (n >= 900)  { out[len++] = 'C'; out[len++] = 'M'; n -= 900; }
    if    (n >= 500)  { out[len++] = 'D'; n -= 500; }
    if    (n >= 400)  { out[len++] = 'C'; out[len++] = 'D'; n -= 400; }
    while (n >= 100)  { out[len++] = 'C'; n -= 100; }
    if    (n >= 90)   { out[len++] = 'X'; out[len++] = 'C'; n -= 90; }
    if    (n >= 50)   { out[len++] = 'L'; n -= 50; }
    if    (n >= 40)   { out[len++] = 'X'; out[len++] = 'L'; n -= 40; }
    while (n >= 10)   { out[len++] = 'X'; n -= 10; }
    if    (n >= 9)    { out[len++] = 'I'; out[len++] = 'X'; n -= 9; }
    if    (n >= 5)    { out[len++] = 'V'; n -= 5; }
    if    (n >= 4)    { out[len++] = 'I'; out[len++] = 'V'; n -= 4; }
    while (n >= 1)    { out[len++] = 'I'; n -= 1; }
    return len;
}

static int64_t value(int32_t c) {
    if (c == 'I') return 1;
    if (c == 'V') return 5;
    if (c == 'X') return 10;
    if (c == 'L') return 50;
    if (c == 'C') return 100;
    if (c == 'D') return 500;
    if (c == 'M') return 1000;
    return 0;
}

static int64_t roman_to_int(const int32_t *r, int len) {
    int64_t total = 0;
    for (int i = 0; i < len; i++) {
        int64_t cur = value(r[i]);
        if (i + 1 < len) {
            int64_t nxt = value(r[i + 1]);
            if (cur < nxt) total -= cur;
            else           total += cur;
        } else {
            total += cur;
        }
    }
    return total;
}

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t raw = k * 2654435769LL + 305419896LL;
        int64_t num = (raw % 3999 + 3999) % 3999 + 1;
        /* One malloc per iter, mirroring Vec.with_capacity(15) in the
         * .kara / .rs versions. Free at end of iter mirrors the per-iter
         * drop of the Vec[char]. */
        int32_t *r = (int32_t *)malloc(15 * sizeof(int32_t));
        int len = int_to_roman(num, r);
        s += roman_to_int(r, len);
        free(r);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
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
    return 0;
}

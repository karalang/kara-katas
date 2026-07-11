/*
 * LeetCode #87 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR).
 * Same batch of K=60000 independent memoized scramble decisions as scramble_string.c;
 * the associative sum reduction is split across a fixed pool of _SC_NPROCESSORS_ONLN
 * pthreads (spawn once, chunk the seed range, join + merge). Raw OS threads, no
 * runtime — the ceiling Kara's auto-par is measured against. This is a compute-bound
 * recursion (the memo is the only allocation), so it parallel-scales well. Sink matches
 * the seq mirrors. Build: clang -O3 scramble_string_par.c -o ... -lpthread
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define LEN 12
#define ITERS 60000

static int scramble(const uint8_t *s1, int64_t i1, const uint8_t *s2, int64_t i2,
                    int64_t len, int64_t *memo, int64_t n) {
    if (len == 0) return 1;
    int64_t key = (i1 * n + i2) * (n + 1) + len;
    if (memo[key] != -1) return memo[key] == 1;
    int equal = 1;
    for (int64_t k = 0; k < len; k++) {
        if (s1[i1 + k] != s2[i2 + k]) { equal = 0; break; }
    }
    if (equal) { memo[key] = 1; return 1; }
    int64_t counts[26] = {0};
    for (int64_t k = 0; k < len; k++) {
        counts[s1[i1 + k] - 97]++;
        counts[s2[i2 + k] - 97]--;
    }
    for (int c = 0; c < 26; c++) {
        if (counts[c] != 0) { memo[key] = 0; return 0; }
    }
    for (int64_t split = 1; split < len; split++) {
        if (scramble(s1, i1, s2, i2, split, memo, n)
            && scramble(s1, i1 + split, s2, i2 + split, len - split, memo, n)) {
            memo[key] = 1;
            return 1;
        }
        if (scramble(s1, i1, s2, i2 + len - split, split, memo, n)
            && scramble(s1, i1 + split, s2, i2, len - split, memo, n)) {
            memo[key] = 1;
            return 1;
        }
    }
    memo[key] = 0;
    return 0;
}

static int64_t one(int64_t len, int64_t seed) {
    uint8_t *s1 = malloc(len * sizeof(uint8_t));
    uint8_t *s2 = malloc(len * sizeof(uint8_t));
    for (int64_t j = 0; j < len; j++)
        s1[j] = (uint8_t)(97 + (j % 8));
    for (int64_t j = 0; j < len; j++)
        s2[j] = s1[(j * 5 + seed) % len];
    int64_t cells = len * len * (len + 1);
    int64_t *memo = malloc(cells * sizeof(int64_t));
    for (int64_t i = 0; i < cells; i++) memo[i] = -1;
    int64_t r = scramble(s1, 0, s2, 0, len, memo, len) ? 1 : 0;
    int64_t h = r;
    for (int64_t i = 0; i < cells; i++)
        h = (h * 131 + (memo[i] + 2)) % 1000000007;
    free(s1);
    free(s2);
    free(memo);
    return h;
}

typedef struct { int64_t start, end, partial; } Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (int64_t i = w->start; i < w->end; i++)
        s += one(LEN, i);
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

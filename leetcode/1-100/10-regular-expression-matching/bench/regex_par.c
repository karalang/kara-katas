/* LeetCode #10 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, regex).
 * Same recursive is_match_at; the K=10M reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 regex_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

#define N 8
#define K_ITERS 10000000LL

static bool is_match_at(const char *s, size_t n, size_t i,
                        const char *p, size_t m, size_t j) {
    if (j == m) {
        return i == n;
    }

    bool first_match = i < n && (p[j] == s[i] || p[j] == '.');

    if (j + 1 < m && p[j + 1] == '*') {
        return is_match_at(s, n, i, p, m, j + 2)
            || (first_match && is_match_at(s, n, i + 1, p, m, j));
    }

    return first_match && is_match_at(s, n, i + 1, p, m, j + 1);
}

static bool is_match(const char *s, const char *p) {
    return is_match_at(s, strlen(s), 0, p, strlen(p), 0);
}

static const char *g_strs[N] = {
    "aa",
    "ab",
    "aab",
    "mississippi",
    "aaaaaaaaaab",
    "aaa",
    "abc",
    "aaab",
};
static const char *g_pats[N] = {
    "a*",
    ".*",
    "c*a*b",
    "mis*is*p*.",
    "a*a*a*a*a*b",
    "ab*a",
    "...",
    "a*b",
};

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % N;
        s += is_match(g_strs[idx], g_pats[idx]) ? 1 : 0;
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

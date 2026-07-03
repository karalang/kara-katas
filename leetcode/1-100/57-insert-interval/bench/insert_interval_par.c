/* LeetCode #57 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * insert_interval). Same linear three-phase insert; the K=1M reduction
 * split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once,
 * chunk, join+merge). Raw OS threads, no runtime — the ceiling auto-par
 * is measured against. Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 insert_interval_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define M_CASES 8
#define N_VALUES 16
#define K_ITERS 1000000LL

typedef struct {
    int64_t start;
    int64_t end;
} Interval;

/* Count-only insert — the par floor skips materializing the output. */
static int64_t insert_interval(const Interval *intervals, int64_t n,
                               int64_t new_start, int64_t new_end) {
    int64_t count = 0;
    int64_t i = 0;
    while (i < n && intervals[i].end < new_start) {
        count++;
        i++;
    }
    while (i < n && intervals[i].start <= new_end) {
        if (intervals[i].start < new_start) new_start = intervals[i].start;
        if (intervals[i].end > new_end) new_end = intervals[i].end;
        i++;
    }
    count++;
    while (i < n) {
        count++;
        i++;
    }
    return count;
}

/* Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31). */
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static Interval *build_case(int64_t seed, int64_t count) {
    Interval *v = (Interval *)malloc(sizeof(Interval) * (size_t)count);
    int64_t state = seed;
    int64_t cursor = 0;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        int64_t gap = (state % 4) + 2;
        state = lcg_next(state);
        int64_t width = (state % 6) + 1;
        int64_t start = cursor + gap;
        int64_t end = start + width;
        v[j].start = start;
        v[j].end = end;
        cursor = end;
    }
    return v;
}

static void pick_new(const Interval *case_, int64_t m, int64_t count,
                     int64_t *out_start, int64_t *out_end) {
    int64_t half = count / 2;
    int64_t st = lcg_next(m * 7919 + 101);
    int64_t lo = st % half;
    st = lcg_next(st);
    int64_t span = st % half;
    int64_t hi = lo + 1 + span;
    if (hi > count - 1) hi = count - 1;
    *out_start = case_[lo].start;
    *out_end = case_[hi].end;
}

typedef struct {
    Interval **sets;
    int64_t *ns;
    int64_t *ne;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % M_CASES;
        s += insert_interval(wk->sets[idx], N_VALUES, wk->ns[idx], wk->ne[idx]);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    Interval **sets = (Interval **)malloc(sizeof(Interval *) * (size_t)M_CASES);
    int64_t ns[M_CASES], ne[M_CASES];
    for (int64_t m = 0; m < M_CASES; m++) {
        sets[m] = build_case(m * 1000003 + 12345, N_VALUES);
        pick_new(sets[m], m, N_VALUES, &ns[m], &ne[m]);
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].sets = sets;
        works[w].ns = ns;
        works[w].ne = ne;
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
    for (int64_t m = 0; m < M_CASES; m++) free(sets[m]);
    free(sets);
    return 0;
}

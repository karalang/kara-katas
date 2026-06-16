/* LeetCode #56 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * merge_intervals). Same merge_intervals (sort-by-first-component +
 * sweep); the K=1M reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink
 * matches the kara/rust/c/go mirrors.
 * Build: clang -O3 merge_intervals_par.c -o … -lpthread */
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

static int cmp_interval(const void *a, const void *b) {
    int64_t xa = ((const Interval *)a)->start;
    int64_t xb = ((const Interval *)b)->start;
    return (xa > xb) - (xa < xb);
}

static int64_t merge_intervals(const Interval *intervals, int64_t n) {
    Interval s[N_VALUES];
    for (int64_t t = 0; t < n; t++) s[t] = intervals[t];
    qsort(s, (size_t)n, sizeof(Interval), cmp_interval);

    if (n == 0) {
        return 0;
    }

    int64_t count = 0;
    int64_t cur_start = s[0].start, cur_end = s[0].end;
    for (int64_t i = 1; i < n; i++) {
        if (s[i].start <= cur_end) {
            if (s[i].end > cur_end) cur_end = s[i].end;
        } else {
            count++;
            cur_start = s[i].start;
            cur_end = s[i].end;
        }
    }
    (void)cur_start;
    count++;
    return count;
}

/* Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31). */
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static Interval *build_case(int64_t seed, int64_t count) {
    Interval *v = (Interval *)malloc(sizeof(Interval) * (size_t)count);
    int64_t state = seed;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        int64_t start = state % 51;
        state = lcg_next(state);
        int64_t width = (state % 10) + 1;
        v[j].start = start;
        v[j].end = start + width;
    }
    return v;
}

typedef struct {
    Interval **sets;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % M_CASES;
        s += merge_intervals(wk->sets[idx], N_VALUES);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    Interval **sets = (Interval **)malloc(sizeof(Interval *) * (size_t)M_CASES);
    for (int64_t m = 0; m < M_CASES; m++) {
        sets[m] = build_case(m * 1000003 + 12345, N_VALUES);
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

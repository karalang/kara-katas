/* LeetCode #18 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, 4Sum).
 * Same sort + two-fix + two-pointer four_sum (allocates+frees the quadruplet
 * rows per iter, returns the count); the K=1M case-rotation reduction split
 * across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is measured
 * against. Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 four_sum_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define M_CASES 8
#define N_VALUES 16
#define K_ITERS 1000000LL

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t four_sum(const int64_t *nums, int64_t n, int64_t target) {
    int64_t *s = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t t = 0; t < n; t++) s[t] = nums[t];
    qsort(s, (size_t)n, sizeof(int64_t), cmp_i64);

    int64_t **result = NULL;
    int64_t count = 0, cap = 0;

    int64_t a = 0;
    while (a < n - 3) {
        if (a > 0 && s[a] == s[a - 1]) { a++; continue; }
        if (s[a] + s[a + 1] + s[a + 2] + s[a + 3] > target) break;
        if (s[a] + s[n - 1] + s[n - 2] + s[n - 3] < target) { a++; continue; }
        int64_t b = a + 1;
        while (b < n - 2) {
            if (b > a + 1 && s[b] == s[b - 1]) { b++; continue; }
            if (s[a] + s[b] + s[b + 1] + s[b + 2] > target) break;
            if (s[a] + s[b] + s[n - 1] + s[n - 2] < target) { b++; continue; }
            int64_t lo = b + 1, hi = n - 1;
            while (lo < hi) {
                int64_t sum = s[a] + s[b] + s[lo] + s[hi];
                if (sum < target) {
                    lo++;
                } else if (sum > target) {
                    hi--;
                } else {
                    if (count == cap) {
                        cap = cap ? cap * 2 : 4;
                        result = (int64_t **)realloc(result, sizeof(int64_t *) * (size_t)cap);
                    }
                    int64_t *row = (int64_t *)malloc(sizeof(int64_t) * 4);
                    row[0] = s[a]; row[1] = s[b]; row[2] = s[lo]; row[3] = s[hi];
                    result[count++] = row;
                    lo++; hi--;
                    while (lo < hi && s[lo] == s[lo - 1]) lo++;
                    while (lo < hi && s[hi] == s[hi + 1]) hi--;
                }
            }
            b++;
        }
        a++;
    }

    for (int64_t r = 0; r < count; r++) free(result[r]);
    free(result);
    free(s);
    return count;
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static int64_t *build_case(int64_t seed, int64_t count) {
    int64_t *v = (int64_t *)malloc(sizeof(int64_t) * (size_t)count);
    int64_t state = seed;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        v[j] = (state % 21) - 10;
    }
    return v;
}

static int64_t target_for(int64_t idx) {
    static const int64_t bag[8] = { -20, -8, -3, 0, 2, 6, 12, 24 };
    return bag[idx];
}

typedef struct {
    int64_t **sets;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % M_CASES;
        s += four_sum(wk->sets[idx], N_VALUES, target_for(idx));
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    int64_t **sets = (int64_t **)malloc(sizeof(int64_t *) * (size_t)M_CASES);
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

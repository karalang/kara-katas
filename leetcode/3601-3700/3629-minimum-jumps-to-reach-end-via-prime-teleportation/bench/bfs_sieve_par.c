/* LeetCode #3629 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, bfs_sieve).
 * Same BFS + prime-factor-sieve min_jumps as bfs_sieve.c; the K=50-call reduction
 * split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is measured
 * against. min_jumps is self-contained + thread-safe (all per-call local allocs);
 * the input array is shared read-only. Sink = 24350 (K=50 × per-call result 487).
 * Build: clang -O3 bfs_sieve_par.c -o … -lpthread */
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct {
    int64_t *data;
    size_t len;
    size_t cap;
} IntVec;

static void intvec_push(IntVec *v, int64_t x) {
    if (v->len == v->cap) {
        size_t new_cap = v->cap == 0 ? 4 : v->cap * 2;
        int64_t *new_data = (int64_t *)realloc(v->data, new_cap * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "realloc failed\n");
            exit(1);
        }
        v->data = new_data;
        v->cap = new_cap;
    }
    v->data[v->len++] = x;
}

static void intvec_free(IntVec *v) {
    free(v->data);
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
}

static IntVec *build_factors(int64_t cap) {
    IntVec *factors = (IntVec *)calloc((size_t)cap + 1, sizeof(IntVec));
    if (!factors) {
        fprintf(stderr, "calloc failed\n");
        exit(1);
    }
    for (int64_t i = 2; i <= cap; i++) {
        if (factors[i].len == 0) {
            for (int64_t j = i; j <= cap; j += i) {
                intvec_push(&factors[j], i);
            }
        }
    }
    return factors;
}

static void free_factors(IntVec *factors, int64_t cap) {
    for (int64_t i = 0; i <= cap; i++) {
        intvec_free(&factors[i]);
    }
    free(factors);
}

static int64_t min_jumps(const int64_t *nums, size_t n) {
    if (n <= 1) {
        return 0;
    }

    int64_t cap = 1;
    for (size_t j = 0; j < n; j++) {
        if (nums[j] > cap) {
            cap = nums[j];
        }
    }

    IntVec *factors = build_factors(cap);

    IntVec *bucket = (IntVec *)calloc((size_t)cap + 1, sizeof(IntVec));
    if (!bucket) {
        fprintf(stderr, "calloc failed\n");
        exit(1);
    }

    for (size_t j = 0; j < n; j++) {
        int64_t v = nums[j];
        if (v >= 2) {
            IntVec *fv = &factors[v];
            for (size_t fi = 0; fi < fv->len; fi++) {
                int64_t p = fv->data[fi];
                intvec_push(&bucket[p], (int64_t)j);
            }
        }
    }

    bool *visited = (bool *)calloc(n, sizeof(bool));
    if (!visited) {
        fprintf(stderr, "calloc failed\n");
        exit(1);
    }
    visited[0] = true;

    int64_t *q_i = (int64_t *)malloc(n * 2 * sizeof(int64_t));
    int64_t *q_d = (int64_t *)malloc(n * 2 * sizeof(int64_t));
    if (!q_i || !q_d) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    size_t q_head = 0;
    size_t q_tail = 0;
    q_i[q_tail] = 0;
    q_d[q_tail] = 0;
    q_tail++;

    int64_t result = -1;
    while (q_head < q_tail) {
        int64_t i = q_i[q_head];
        int64_t d = q_d[q_head];
        q_head++;

        if ((size_t)i == n - 1) {
            result = d;
            break;
        }
        if (i > 0 && !visited[(size_t)(i - 1)]) {
            visited[(size_t)(i - 1)] = true;
            q_i[q_tail] = i - 1;
            q_d[q_tail] = d + 1;
            q_tail++;
        }
        if (i + 1 < (int64_t)n && !visited[(size_t)(i + 1)]) {
            visited[(size_t)(i + 1)] = true;
            q_i[q_tail] = i + 1;
            q_d[q_tail] = d + 1;
            q_tail++;
        }
        int64_t v = nums[(size_t)i];
        if (v >= 2 && factors[v].len > 0 && factors[v].data[0] == v) {
            IntVec *indices = &bucket[v];
            for (size_t bi = 0; bi < indices->len; bi++) {
                int64_t j = indices->data[bi];
                if (!visited[(size_t)j]) {
                    visited[(size_t)j] = true;
                    q_i[q_tail] = j;
                    q_d[q_tail] = d + 1;
                    q_tail++;
                }
            }
            indices->len = 0;
        }
    }

    free(q_i);
    free(q_d);
    free(visited);
    for (int64_t p = 0; p <= cap; p++) {
        intvec_free(&bucket[p]);
    }
    free(bucket);
    free_factors(factors, cap);

    return result;
}

#define N 50000
#define ITERS 50

typedef struct {
    const int64_t *data;
    long start, end;
    int64_t partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    int64_t s = 0;
    for (long k = w->start; k < w->end; k++) {
        s += min_jumps(w->data, (size_t)N);
    }
    w->partial = s;
    return NULL;
}

int main(void) {
    int64_t *data = (int64_t *)malloc((size_t)N * sizeof(int64_t));
    for (size_t i = 0; i < (size_t)N; i++) {
        data[i] = ((int64_t)i * 7919 + 13) % 999983 + 2;
    }

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

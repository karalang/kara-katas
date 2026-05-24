// Benchmark workload — BFS + sieve solution to LeetCode #3629.
// C mirror of bench/bfs_sieve.kara and bench/bfs_sieve.rs. Same N, K,
// seeding scheme, sink formula — see those files' headers for rationale.
//
// Built via `clang -O3` in bench.sh.

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    int64_t *data;
    size_t len;
    size_t cap;
} IntVec;

static void intvec_init(IntVec *v) {
    v->data = NULL;
    v->len = 0;
    v->cap = 0;
}

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

int main(void) {
    const size_t N = 50000;
    const int k_iters = 3;

    int64_t *data = (int64_t *)malloc(N * sizeof(int64_t));
    if (!data) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }
    for (size_t i = 0; i < N; i++) {
        data[i] = ((int64_t)i * 7919 + 13) % 999983 + 2;
    }

    int64_t sum = 0;
    for (int k = 0; k < k_iters; k++) {
        sum += min_jumps(data, N);
    }
    printf("%lld\n", (long long)sum);

    free(data);
    return 0;
}

// Benchmark for #826: Most Profit Assigning Work -- the ★ arm (two sorted sweeps).
//
// Mirrors max_profit_assignment.kara: the jobs paired and sorted by
// difficulty (then profit) and a copy of the workers sorted, then one
// pointer walks the jobs as the abilities grow, keeping the best profit
// among the jobs passed. The pairs and the copy are fresh arrays each
// call, as the Kāra program's Vecs are; the sorts are the C library's
// qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t d, p;
} Job;

static int cmp_job(const void *a, const void *b) {
    const Job *x = a, *y = b;
    if (x->d != y->d) return x->d < y->d ? -1 : 1;
    if (x->p != y->p) return x->p < y->p ? -1 : 1;
    return 0;
}

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return x < y ? -1 : x > y;
}

static int64_t max_profit_assignment(const int64_t *difficulty, const int64_t *profit, int64_t n,
                                     const int64_t *worker, int64_t m) {
    Job *jobs = malloc((size_t)n * sizeof(Job));
    for (int64_t i = 0; i < n; i++) jobs[i] = (Job){difficulty[i], profit[i]};
    qsort(jobs, (size_t)n, sizeof(Job), cmp_job);
    int64_t *abilities = malloc((size_t)m * sizeof(int64_t));
    memcpy(abilities, worker, (size_t)m * sizeof(int64_t));
    qsort(abilities, (size_t)m, sizeof(int64_t), cmp_i64);
    int64_t next = 0, best = 0, total = 0;
    for (int64_t j = 0; j < m; j++) {
        while (next < n && jobs[next].d <= abilities[j]) {
            if (jobs[next].p > best) best = jobs[next].p;
            next++;
        }
        total += best;
    }
    free(jobs);
    free(abilities);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t *draw(int64_t *seed, int64_t count) {
    int64_t *v = malloc((size_t)count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) v[i] = 1 + next_random(seed) % 100000;
    return v;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 2000;
    int64_t seed = 826;
    int64_t *difficulties[64], *profits[64], *workers[64];
    for (int64_t g = 0; g < count; g++) {
        difficulties[g] = draw(&seed, 10000);
        profits[g] = draw(&seed, 10000);
        workers[g] = draw(&seed, 10000);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t r = max_profit_assignment(difficulties[g], profits[g], 10000, workers[g], 10000);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    printf("%lld rounds of %lld cases: total %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}

// LeetCode #2136: Earliest Possible Day of Full Bloom -- the benchmark,
// the same algorithm as bloom.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static const int64_t *by_grow;

static int longest_first(const void *x, const void *y) {
    int64_t a = by_grow[*(const int64_t *)x], b = by_grow[*(const int64_t *)y];
    return (a < b) - (a > b);
}

static int64_t earliest_full_bloom(const int64_t *plant_time, const int64_t *grow_time, int64_t n,
                                   int64_t *order) {
    for (int64_t i = 0; i < n; i++) order[i] = i;
    by_grow = grow_time;
    qsort(order, n, sizeof(int64_t), longest_first);
    int64_t planted = 0, bloom = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t i = order[k];
        planted += plant_time[i];
        if (planted + grow_time[i] > bloom) bloom = planted + grow_time[i];
    }
    return bloom;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2136;
    int64_t *plants[10], *grows[10];
    for (int g = 0; g < 10; g++) {
        plants[g] = malloc(N * sizeof(int64_t));
        grows[g] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) {
            plants[g][i] = next_random(&seed) % 10000 + 1;
            grows[g][i] = next_random(&seed) % 10000 + 1;
        }
    }
    int64_t *order = malloc(N * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int g = 0; g < 10; g++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            plants[g][at] = next_random(&seed) % 10000 + 1;
            grows[g][at] = next_random(&seed) % 10000 + 1;
            int64_t day = earliest_full_bloom(plants[g], grows[g], N, order);
            total += day;
            check = (check * 31 + day + round) % 1000000007;
        }
    }
    printf("100 solves: %lld days in all, checksum %lld\n", (long long)total, (long long)check);
    free(order);
    for (int g = 0; g < 10; g++) {
        free(plants[g]);
        free(grows[g]);
    }
    return 0;
}

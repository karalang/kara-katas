// LeetCode #1029: Two City Scheduling -- bench
// Mirrors ./two_city.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_saving(const void *x, const void *y) {
    const int64_t *a = x, *b = y;
    int64_t da = a[0] - a[1], db = b[0] - b[1];
    return (da > db) - (da < db);
}

static int64_t two_city_sched_cost(const int64_t (*costs)[2], int n) {
    int64_t (*order)[2] = malloc(sizeof(int64_t[2]) * n);
    memcpy(order, costs, sizeof(int64_t[2]) * n);
    qsort(order, n, sizeof(int64_t[2]), by_saving);
    int half = n / 2;
    int64_t total = 0;
    for (int i = 0; i < n; i++) total += i < half ? order[i][0] : order[i][1];
    free(order);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 1000, rounds = 100;
    int64_t seed = 1029;
    static int64_t cases[1000][100][2];
    for (int k = 0; k < count; k++) {
        for (int p = 0; p < 100; p++) {
            int64_t a = next_random(&seed) % 1000 + 1;
            int64_t b = next_random(&seed) % 1000 + 1;
            cases[k][p][0] = a;
            cases[k][p][1] = b;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t answer = two_city_sched_cost((const int64_t (*)[2])cases[k], 100);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    printf("%d cases of 100 people, %d rounds: sum %lld, checksum %lld\n", count, rounds,
           (long long)total, (long long)check);
    return 0;
}

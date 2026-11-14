// LeetCode #2140: Solving Questions With Brainpower -- the benchmark, the
// same algorithm as brainpower.kara; each question its own two-value
// allocation, as a `Vec[Vec[i64]]` holds it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t most_points(int64_t **questions, int64_t n, int64_t *best) {
    best[n] = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t next = i + 1 + questions[i][1];
        if (next > n) next = n;
        int64_t solve = questions[i][0] + best[next];
        best[i] = best[i + 1] > solve ? best[i + 1] : solve;
    }
    return best[0];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2140;
    int64_t **lists[10];
    for (int l = 0; l < 10; l++) {
        lists[l] = malloc(N * sizeof(int64_t *));
        for (int64_t i = 0; i < N; i++) {
            lists[l][i] = malloc(2 * sizeof(int64_t));
            lists[l][i][0] = next_random(&seed) % 100000 + 1;
            lists[l][i][1] = next_random(&seed) % 21;
        }
    }
    int64_t *best = malloc((N + 1) * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int l = 0; l < 10; l++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            lists[l][at][0] = next_random(&seed) % 100000 + 1;
            lists[l][at][1] = next_random(&seed) % 21;
            int64_t points = most_points(lists[l], N, best);
            total += points;
            check = (check * 31 + points + round) % 1000000007;
        }
    }
    printf("200 solves: %lld points in all, checksum %lld\n", (long long)total, (long long)check);
    free(best);
    for (int l = 0; l < 10; l++) {
        for (int64_t i = 0; i < N; i++) free(lists[l][i]);
        free(lists[l]);
    }
    return 0;
}

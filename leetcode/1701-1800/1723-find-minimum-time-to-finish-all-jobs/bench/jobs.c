// LeetCode #1723: Find Minimum Time to Finish All Jobs -- the bench
// (jobs.kara): each job, the longest first, tried on every worker by
// backtracking, a branch cut once it cannot beat the best finish found,
// and only the first idle worker tried.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 12
#define COUNT 100
#define ROUNDS 5

static void place(const int32_t *jobs, int n, int i, int32_t *loads, int k, int32_t *best) {
    if (i == n) {
        int32_t most = loads[0];
        for (int w = 1; w < k; w++) {
            if (loads[w] > most) {
                most = loads[w];
            }
        }
        *best = most;
        return;
    }
    for (int w = 0; w < k; w++) {
        if (loads[w] + jobs[i] < *best) {
            loads[w] += jobs[i];
            place(jobs, n, i + 1, loads, k, best);
            loads[w] -= jobs[i];
        }
        if (loads[w] == 0) {
            break;
        }
    }
}

static int descending(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (y > x) - (y < x);
}

static int32_t minimum_time_required(const int32_t *jobs, int n, int k) {
    int32_t order[N];
    int32_t loads[N] = {0};
    int32_t total = 0;
    for (int i = 0; i < n; i++) {
        order[i] = jobs[i];
        total += jobs[i];
    }
    qsort(order, n, sizeof order[0], descending);
    int32_t best = total + 1;
    place(order, n, 0, loads, k, &best);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    static int32_t jobs[COUNT][N];
    static int ks[COUNT];
    int64_t seed = 1723;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            jobs[c][i] = (int32_t)(wide(&seed) % 10000000 + 1);
        }
        ks[c] = (int)(next_random(&seed) % 11 + 2);
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = minimum_time_required(jobs[c], N, ks[c]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d jobs, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum,
           (long long)check);
    return 0;
}

// LeetCode #2141: Maximum Running Time of N Computers -- the benchmark, the
// same algorithm as running.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t max_run_time(int64_t n, const int64_t *batteries, int64_t len) {
    int64_t total = 0;
    for (int64_t i = 0; i < len; i++) total += batteries[i];
    int64_t low = 0, high = total / n;
    while (low < high) {
        int64_t mid = (low + high + 1) / 2;
        int64_t usable = 0;
        for (int64_t i = 0; i < len; i++) usable += batteries[i] < mid ? batteries[i] : mid;
        if (usable >= n * mid) low = mid;
        else high = mid - 1;
    }
    return low;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2141;
    int64_t *fleets[10];
    for (int f = 0; f < 10; f++) {
        fleets[f] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) {
            int64_t hi = next_random(&seed);
            fleets[f][i] = (hi * 32768 + next_random(&seed)) % 1000000000 + 1;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int f = 0; f < 10; f++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            hi = next_random(&seed);
            fleets[f][at] = (hi * 32768 + next_random(&seed)) % 1000000000 + 1;
            int64_t minutes = max_run_time(10000 * (f + 1), fleets[f], N);
            total += minutes;
            check = (check * 31 + minutes % 1000000007 + round) % 1000000007;
        }
    }
    printf("200 solves: %lld minutes in all, checksum %lld\n", (long long)total, (long long)check);
    for (int f = 0; f < 10; f++) free(fleets[f]);
    return 0;
}

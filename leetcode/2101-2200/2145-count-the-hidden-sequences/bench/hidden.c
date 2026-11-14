// LeetCode #2145: Count the Hidden Sequences -- the benchmark, the same
// algorithm as hidden.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define W 20

static int64_t number_of_arrays(const int64_t *differences, int64_t n, int64_t lower, int64_t upper) {
    int64_t at = 0, lowest = 0, highest = 0;
    for (int64_t i = 0; i < n; i++) {
        at += differences[i];
        if (at < lowest) lowest = at;
        if (at > highest) highest = at;
    }
    int64_t count = (upper - lower) - (highest - lowest) + 1;
    return count > 0 ? count : 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2145;
    int64_t *walks[W];
    for (int w = 0; w < W; w++) {
        walks[w] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) walks[w][i] = next_random(&seed) % 21 - 10;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int w = 0; w < W; w++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            walks[w][at] = next_random(&seed) % 21 - 10;
            int64_t count = number_of_arrays(walks[w], N, -100000, 100000);
            total += count;
            check = (check * 31 + count + round) % 1000000007;
        }
    }
    printf("4000 solves: %lld sequences in all, checksum %lld\n", (long long)total, (long long)check);
    for (int w = 0; w < W; w++) free(walks[w]);
    return 0;
}

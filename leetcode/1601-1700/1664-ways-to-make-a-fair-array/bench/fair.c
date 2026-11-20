// LeetCode #1664 bench: the ★ arm, one pass with running sums.
//
// 20 arrays of 10^5 values from 1 to 2, LeetCode's largest length, drawn
// first; then each is answered 50 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t ways_to_make_fair(const int32_t *nums, int64_t n) {
    int32_t total[2] = {0, 0};
    for (int64_t i = 0; i < n; i++) total[i % 2] += nums[i];
    int32_t before[2] = {0, 0};
    int32_t ways = 0;
    for (int64_t i = 0; i < n; i++) {
        int p = (int)(i % 2);
        int32_t after[2] = {total[0] - before[0], total[1] - before[1]};
        after[p] -= nums[i];
        if (before[0] + after[1] == before[1] + after[0]) ways++;
        before[p] += nums[i];
    }
    return ways;
}

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 20, N = 100000, ROUNDS = 50 };
    seed = 1664;
    int32_t *arrays[COUNT];
    for (int c = 0; c < COUNT; c++) {
        arrays[c] = malloc(N * sizeof(int32_t));
        for (int i = 0; i < N; i++) arrays[c][i] = (int32_t)(next_random() % 2 + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = ways_to_make_fair(arrays[c], N);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: %lld fair removals, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    for (int c = 0; c < COUNT; c++) free(arrays[c]);
    return 0;
}

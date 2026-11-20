// LeetCode #1674: Minimum Moves to Make Array Complementary -- the bench's C
// mirror: the ★ arm on 100 arrays of 100000 values with limits up to
// 100000, all drawn first, each answered 20 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 100
#define N 100000
#define ROUNDS 20

static int32_t min_moves(const int32_t *nums, int64_t n, int64_t limit) {
    int64_t *delta = calloc((size_t)(2 * limit + 2), sizeof *delta);
    for (int64_t i = 0; i < n / 2; i++) {
        int64_t x = nums[i], y = nums[n - 1 - i];
        int64_t a = x < y ? x : y, b = x < y ? y : x;
        delta[2] += 2;
        delta[a + 1] -= 1;
        delta[a + b] -= 1;
        delta[a + b + 1] += 1;
        delta[b + limit + 1] += 1;
    }
    int64_t best = n, moves = 0;
    for (int64_t sum = 2; sum <= 2 * limit; sum++) {
        moves += delta[sum];
        if (moves < best) best = moves;
    }
    free(delta);
    return (int32_t)best;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1674;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[ARRAYS][N];
    static int64_t limits[ARRAYS];
    for (int a = 0; a < ARRAYS; a++) {
        limits[a] = (next_random() * 32768 + next_random()) % 100000 + 1;
        for (int i = 0; i < N; i++) nums[a][i] = (int32_t)((next_random() * 32768 + next_random()) % limits[a] + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int64_t moves = min_moves(nums[a], N, limits[a]);
            total += moves;
            check = (check * 31 + moves + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: %lld moves, checksum %lld\n", ARRAYS, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}

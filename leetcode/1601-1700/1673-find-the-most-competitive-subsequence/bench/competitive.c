// LeetCode #1673: Find the Most Competitive Subsequence -- the bench's C
// mirror: the ★ arm on 50 arrays of 100000 values up to 10^9, each with a
// random k, all drawn first, each answered 20 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 50
#define N 100000
#define ROUNDS 20

// the answer in `stack`, its length returned
static int64_t most_competitive(const int32_t *nums, int64_t n, int64_t k, int32_t *stack) {
    int64_t len = 0;
    for (int64_t i = 0; i < n; i++) {
        while (len > 0 && stack[len - 1] > nums[i] && len - 1 + n - i >= k) len--;
        if (len < k) stack[len++] = nums[i];
    }
    return len;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1673;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[ARRAYS][N];
    static int64_t ks[ARRAYS];
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) nums[a][i] = (int32_t)((next_random() * 32768 + next_random()) % 1000000000);
        ks[a] = (next_random() * 32768 + next_random()) % N + 1;
    }
    int64_t chosen = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int32_t *stack = malloc((size_t)ks[a] * sizeof *stack);
            int64_t len = most_competitive(nums[a], N, ks[a], stack);
            chosen += len;
            check = (check * 31 + stack[0] + stack[len - 1] + r) % 1000000007;
            free(stack);
        }
    }
    printf("%d arrays of %d values, %d rounds: %lld chosen, checksum %lld\n", ARRAYS, N, ROUNDS, (long long)chosen, (long long)check);
    return 0;
}

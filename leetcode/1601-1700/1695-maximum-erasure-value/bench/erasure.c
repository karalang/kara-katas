// LeetCode #1695: Maximum Erasure Value -- the bench's C mirror: the ★ arm
// on 50 random arrays of 100000 values up to 10^4, all drawn first, each
// answered 60 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define ROUNDS 60
#define N 100000

static int32_t maximum_unique_subarray(const int32_t *nums, int64_t n) {
    int64_t *last = malloc(10001 * sizeof *last);
    for (int i = 0; i <= 10000; i++) {
        last[i] = -1;
    }
    int32_t *prefix = calloc((size_t)n + 1, sizeof *prefix);
    int64_t start = 0;
    int32_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        int32_t v = nums[i];
        prefix[i + 1] = prefix[i] + v;
        if (last[v] + 1 > start) {
            start = last[v] + 1;
        }
        last[v] = i;
        int32_t sum = prefix[i + 1] - prefix[start];
        if (sum > best) {
            best = sum;
        }
    }
    free(last);
    free(prefix);
    return best;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1695;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *arrays = malloc((size_t)COUNT * N * sizeof *arrays);
    for (int64_t i = 0; i < (int64_t)COUNT * N; i++) {
        arrays[i] = (int32_t)(next_random() % 10000 + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = maximum_unique_subarray(arrays + (int64_t)c * N, N);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    free(arrays);
    return 0;
}

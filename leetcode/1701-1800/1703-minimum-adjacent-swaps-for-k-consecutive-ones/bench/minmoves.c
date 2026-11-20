// LeetCode #1703: Minimum Adjacent Swaps for K Consecutive Ones -- the
// bench's C mirror: the ★ arm on 50 random arrays of 100000 values, each
// with a random k, all drawn first, each answered 40 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define ROUNDS 40
#define N 100000

// each window of k ones about its median, q[j] = p[j] - j, by prefix sums
static int32_t min_moves(const int32_t *nums, int64_t n, int32_t k) {
    int64_t *q = malloc((size_t)n * sizeof *q);
    int64_t *prefix = malloc(((size_t)n + 1) * sizeof *prefix);
    int64_t len = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 1) {
            q[len] = i - len;
            len++;
        }
    }
    prefix[0] = 0;
    for (int64_t j = 0; j < len; j++) {
        prefix[j + 1] = prefix[j] + q[j];
    }
    int64_t best = INT64_MAX;
    for (int64_t i = 0; i <= len - k; i++) {
        int64_t end = i + k;
        int64_t m = i + k / 2;
        int64_t left = q[m] * (m - i) - (prefix[m] - prefix[i]);
        int64_t right = (prefix[end] - prefix[m + 1]) - q[m] * (end - m - 1);
        if (left + right < best) {
            best = left + right;
        }
    }
    free(q);
    free(prefix);
    return (int32_t)best;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1703;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *arrays = malloc((size_t)COUNT * N * sizeof *arrays);
    int32_t ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        // each value a 1 with a chance of its array's own, 1 to 10 in 10
        int64_t lean = next_random() % 10 + 1;
        int64_t ones = 0;
        for (int64_t i = 0; i < N; i++) {
            int32_t v = next_random() % 10 < lean ? 1 : 0;
            arrays[(int64_t)c * N + i] = v;
            ones += v;
        }
        ks[c] = (int32_t)(next_random() % ones + 1);
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = min_moves(arrays + (int64_t)c * N, N, ks[c]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    free(arrays);
    return 0;
}

// LeetCode #1696: Jump Game VI -- the bench's C mirror: the ★ arm on 50
// random arrays of 100000 values from -10^4 to 10^4, each with a random k
// up to 100000, all drawn first, each answered 20 times. C has no deque;
// the indexes only go on at the back, so an array with a head and a tail
// holds them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define ROUNDS 20
#define N 100000

static int32_t max_result(const int32_t *nums, int64_t n, int64_t k) {
    int32_t *best = calloc((size_t)n, sizeof *best);
    int64_t *reach = malloc((size_t)n * sizeof *reach);
    int64_t head = 0, tail = 0;
    best[0] = nums[0];
    reach[tail++] = 0;
    for (int64_t i = 1; i < n; i++) {
        if (reach[head] < i - k) {
            head++;
        }
        best[i] = nums[i] + best[reach[head]];
        while (tail > head && best[reach[tail - 1]] <= best[i]) {
            tail--;
        }
        reach[tail++] = i;
    }
    int32_t answer = best[n - 1];
    free(best);
    free(reach);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1696;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *arrays = malloc((size_t)COUNT * N * sizeof *arrays);
    int64_t ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) {
            arrays[(int64_t)c * N + i] = (int32_t)(next_random() % 20001 - 10000);
        }
        int64_t hi = next_random();
        ks[c] = (hi * 32768 + next_random()) % N + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = max_result(arrays + (int64_t)c * N, N, ks[c]);
            total += answer;
            check = ((check * 31 + answer + r) % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    free(arrays);
    return 0;
}

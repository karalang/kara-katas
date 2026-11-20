// LeetCode #1692: Count Ways to Distribute Candies -- the bench's C mirror:
// the ★ arm on 200 problems of 1000 candies, each with a random number of
// bags up to 1000, all drawn first, each answered 8 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 200
#define ROUNDS 8
#define N 1000

static int32_t ways_to_distribute(int32_t n, int32_t k) {
    const int64_t modulus = 1000000007;
    int64_t *ways = calloc((size_t)k + 1, sizeof *ways);
    ways[0] = 1;
    for (int64_t i = 1; i <= n; i++) {
        for (int64_t j = i < k ? i : k; j >= 1; j--) {
            ways[j] = (j * ways[j] + ways[j - 1]) % modulus;
        }
        ways[0] = 0;
    }
    int32_t answer = (int32_t)ways[k];
    free(ways);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1692;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t bags[COUNT];
    for (int i = 0; i < COUNT; i++) {
        bags[i] = (int32_t)(next_random() % N + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t answer = ways_to_distribute(N, bags[i]);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d candies, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}

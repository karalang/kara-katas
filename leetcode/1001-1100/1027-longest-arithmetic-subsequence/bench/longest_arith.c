// LeetCode #1027: Longest Arithmetic Subsequence -- bench
// Mirrors ./longest_arith.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_arith_seq_length(const int64_t *nums, int n) {
    int64_t *run = calloc((size_t)n * 1001, sizeof(int64_t));
    int64_t best = 2;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            int64_t d = nums[i] - nums[j] + 500;
            int64_t before = run[(size_t)j * 1001 + d];
            int64_t length = before > 0 ? before + 1 : 2;
            if (length > run[(size_t)i * 1001 + d]) run[(size_t)i * 1001 + d] = length;
            if (length > best) best = length;
        }
    }
    free(run);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int count = 40, rounds = 3;
    const int64_t tops[4] = {5, 50, 500, 500};
    int64_t seed = 1027;
    int64_t *arrays = malloc(sizeof(int64_t) * count * 1000);
    for (int k = 0; k < count; k++)
        for (int m = 0; m < 1000; m++) arrays[k * 1000 + m] = next_random(&seed) % (tops[k % 4] + 1);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t answer = longest_arith_seq_length(arrays + k * 1000, 1000);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    printf("%d arrays of 1000 values, %d rounds: sum %lld, checksum %lld\n", count, rounds, (long long)total,
           (long long)check);
    return 0;
}

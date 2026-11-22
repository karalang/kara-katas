// LeetCode #2859: Sum of Values at Indices With K Set Bits -- the
// bench: the ★ arm over 2000 arrays of 1000 values up to 10^5,
// LeetCode's most, with k up to 10, all drawn first, then each answered
// 100 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t sum_indices_with_k_set_bits(const int64_t *nums, int64_t n, int64_t k) {
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++)
        if (__builtin_popcountll((uint64_t)i) == k) sum += nums[i];
    return sum;
}

static int64_t seed = 2859;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 2000, rounds = 100, n = 1000;
    int64_t *nums = malloc(sizeof(int64_t) * count * n);
    int64_t ks[2000];
    for (int64_t c = 0; c < count; c++) {
        ks[c] = next_random() % 11;
        for (int64_t i = 0; i < n; i++) nums[c * n + i] = wide() % 100000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t sum = sum_indices_with_k_set_bits(nums + c * n, n, ks[c]);
            total += sum;
            check = (check * 31 + sum + r) % 1000000007;
        }
    }
    printf("%lld arrays, %lld rounds: sums total %lld, checksum %lld\n", (long long)count, (long long)rounds, (long long)total, (long long)check);
    free(nums);
    return 0;
}

// LeetCode #2892: Minimizing Array After Replacing Pairs With Their
// Product -- the bench, as
// product.kara: 50 arrays of 10^5 values, each with its k, answered 20
// times by the greedy arm.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_array_length(const int64_t *nums, int64_t n, int64_t k) {
    for (int64_t i = 0; i < n; i++)
        if (nums[i] == 0) return 1;
    int64_t runs = 1, product = nums[0];
    for (int64_t i = 1; i < n; i++) {
        int64_t x = nums[i];
        if (product * x <= k) {
            product *= x;
        } else {
            runs++;
            product = x;
        }
    }
    return runs;
}

static int64_t seed = 2892;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 20, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    int64_t ks[50];
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = arrays + c * n;
        for (int64_t i = 0; i < n; i++) nums[i] = next_random() % 2 == 0 ? 1 : next_random() % 1000 + 1;
        if (c % 10 == 0) nums[n - 1 - c] = 0;
        ks[c] = wide() % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t length = min_array_length(arrays + c * n, n, ks[c]);
            total += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: lengths total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}

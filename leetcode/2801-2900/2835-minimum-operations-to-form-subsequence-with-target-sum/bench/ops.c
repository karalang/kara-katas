// LeetCode #2835: Minimum Operations to Form Subsequence With Target Sum
// -- the bench, mirrored from ops.kara: counts by bit, low to high.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t min_operations(const int64_t *nums, int64_t n, int64_t target) {
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) sum += nums[i];
    if (sum < target) return -1;
    int64_t count[32] = {0};
    for (int64_t i = 0; i < n; i++) count[__builtin_ctzll((unsigned long long)nums[i])]++;
    int64_t ops = 0;
    for (int64_t i = 0; i < 31; i++) {
        if ((target >> i) & 1) {
            if (count[i] > 0) {
                count[i]--;
            } else {
                int64_t j = i + 1;
                while (count[j] == 0) j++;
                ops += j - i;
                count[j]--;
                for (int64_t k = i; k < j; k++) count[k]++;
            }
        }
        count[i + 1] += count[i] / 2;
    }
    return ops;
}

int main(void) {
    const int64_t count = 2000, rounds = 200, n = 1000;
    int64_t seed = 2835;
    int64_t *nums = malloc(sizeof(int64_t) * count * n);
    int64_t *targets = malloc(sizeof(int64_t) * count);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) nums[c * n + i] = (int64_t)1 << (next_random(&seed) % 15 + 16);
        int64_t hi = next_random(&seed);
        targets[c] = (hi * 32768 + next_random(&seed)) % 2147483647 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t ops = min_operations(nums + c * n, n, targets[c]);
            total += ops;
            check = (check * 31 + ops + 1 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: operations total %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(nums); free(targets);
    return 0;
}

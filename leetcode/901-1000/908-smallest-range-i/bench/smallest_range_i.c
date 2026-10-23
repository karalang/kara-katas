// LeetCode #908: Smallest Range I -- bench program, C.
//
// The largest and smallest values, over 500,000 numbers up to 10^4 built
// once. Each round scores them with a k that changes from round to round,
// folds the score into a checksum and changes one number.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t smallest_range_i(const int64_t *nums, int64_t n, int64_t k) {
    int64_t lo = nums[0], hi = nums[0];
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] < lo) lo = nums[i];
        if (nums[i] > hi) hi = nums[i];
    }
    int64_t score = hi - lo - 2 * k;
    return score > 0 ? score : 0;
}

static int64_t seed = 908;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 500000;
    int64_t rounds = 500;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) nums[i] = next_random() % 10001;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t got = smallest_range_i(nums, n, round * 37 % 5001);
        total += got;
        check = (check * 31 + got) % 1000000007;
        nums[round * 7919 % n] = next_random() % 10001;
    }
    printf("%lld rounds over %lld numbers: scores summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    free(nums);
    return 0;
}

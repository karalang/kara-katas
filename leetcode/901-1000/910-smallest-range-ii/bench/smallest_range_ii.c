// LeetCode #910: Smallest Range II -- bench program, C.
//
// The sorted values split in two, over 500,000 numbers up to 10^4 built
// once. Each round solves them with a k that changes from round to round,
// folds the score into a checksum and changes one number.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t smallest_range_ii(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *a = malloc(sizeof(int64_t) * n);
    memcpy(a, nums, sizeof(int64_t) * n);
    qsort(a, n, sizeof(int64_t), compare);
    int64_t best = a[n - 1] - a[0];
    for (int64_t i = 0; i < n - 1; i++) {
        int64_t hi = a[i] + k > a[n - 1] - k ? a[i] + k : a[n - 1] - k;
        int64_t lo = a[0] + k < a[i + 1] - k ? a[0] + k : a[i + 1] - k;
        if (hi - lo < best) best = hi - lo;
    }
    free(a);
    return best;
}

static int64_t seed = 910;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 500000;
    int64_t rounds = 40;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) nums[i] = next_random() % 10001;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t got = smallest_range_ii(nums, n, round * 373 % 5001);
        total += got;
        check = (check * 31 + got) % 1000000007;
        nums[round * 7919 % n] = next_random() % 10001;
    }
    printf("%lld rounds over %lld numbers: scores summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    free(nums);
    return 0;
}

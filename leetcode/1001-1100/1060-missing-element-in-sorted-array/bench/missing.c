// LeetCode #1060: Missing Element in Sorted Array -- the benchmark, the
// same algorithm as missing.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static inline int64_t missing(const int64_t *nums, int64_t i) { return nums[i] - nums[0] - i; }

static int64_t missing_element(const int64_t *nums, int64_t n, int64_t k) {
    int64_t last = n - 1;
    if (missing(nums, last) < k) return nums[last] + k - missing(nums, last);
    // missing(lo) < k <= missing(hi)
    int64_t lo = 0, hi = last;
    while (hi - lo > 1) {
        int64_t mid = lo + (hi - lo) / 2;
        if (missing(nums, mid) < k) lo = mid;
        else hi = mid;
    }
    return nums[lo] + k - missing(nums, lo);
}

static int64_t seed = 1060;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    // 50 arrays of 50000 values, built once; 200000 values of k each
    int64_t calls = 0, sum = 0, check = 0;
    int64_t *nums = malloc(50000 * sizeof *nums);
    for (int64_t a = 0; a < 50; a++) {
        nums[0] = next_random() % 100 + 1;
        for (int64_t i = 1; i < 50000; i++) {
            int64_t gap = 1 + next_random() % (2 + a * 3);
            nums[i] = nums[i - 1] + gap;
        }
        int64_t span = nums[49999] - nums[0] - 49999;
        for (int64_t j = 0; j < 200000; j++) {
            int64_t hi = next_random() * 32768;
            int64_t k = 1 + (hi + next_random()) % (span + 1000);
            int64_t answer = missing_element(nums, 50000, k);
            sum += answer;
            check = (check * 31 + answer % 1000003) % 1000000007;
            calls++;
        }
    }
    free(nums);
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}

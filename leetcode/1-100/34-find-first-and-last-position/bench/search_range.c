/* LeetCode #34 bench — C (mirror of search_range.kara).
 *
 * Two-bounds style: lower_bound + upper_bound per query over a fixed sorted array
 * with duplicate runs, TOTAL queries with cycling targets, both endpoints folded
 * into a checksum. The no-allocation floor: the array is one heap block, each
 * bound search is pure index arithmetic.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t lower_bound(const int64_t *nums, int64_t len, int64_t target) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

static int64_t upper_bound(const int64_t *nums, int64_t len, int64_t target) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (nums[mid] <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main(void) {
    const int64_t n = 4096;
    const int64_t run = 4;
    const int64_t total = 14000000;
    const int64_t modulus = 1000000007;

    int64_t *nums = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t p = 0; p < n; p++) {
        nums[p] = 2 * (p / run);
    }

    int64_t span = 2 * n;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t target = k % span;
        int64_t lo = lower_bound(nums, n, target);
        int64_t first = -1, last = -1;
        if (lo < n && nums[lo] == target) {
            first = lo;
            last = upper_bound(nums, n, target) - 1;
        }
        acc = (acc * 31 + (first + 1)) % modulus;
        acc = (acc * 31 + (last + 1)) % modulus;
    }

    free(nums);
    printf("%lld\n", (long long)acc);
    return 0;
}

/* LeetCode #35 bench — C (mirror of search_insert.kara).
 *
 * Half-open lower_bound style: one search_insert (first index >= target) per query
 * over a fixed strictly-increasing array of distinct values, TOTAL queries with
 * cycling targets, each index folded into a checksum. The no-allocation floor: the
 * array is one heap block, the search is pure index arithmetic.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t search_insert(const int64_t *nums, int64_t len, int64_t target) {
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

int main(void) {
    const int64_t n = 4096;
    const int64_t total = 14000000;
    const int64_t modulus = 1000000007;

    int64_t *nums = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t p = 0; p < n; p++) {
        nums[p] = 2 * p;
    }

    int64_t span = 2 * n;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t target = k % span;
        int64_t idx = search_insert(nums, n, target);
        acc = (acc * 31 + idx) % modulus;
    }

    free(nums);
    printf("%lld\n", (long long)acc);
    return 0;
}

/* LeetCode #33 bench — C (mirror of search_rotated.kara).
 *
 * One-pass modified binary search over a fixed rotated-sorted array, TOTAL
 * searches with cycling targets, folded into a checksum. The no-allocation
 * floor: the array is one heap block, the search is pure index arithmetic.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t search(const int64_t *nums, int64_t len, int64_t target) {
    int64_t lo = 0, hi = len - 1;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t m = nums[mid];
        if (m == target) {
            return mid;
        }
        if (nums[lo] <= m) {
            if (nums[lo] <= target && target < m) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else if (m < target && target <= nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

int main(void) {
    const int64_t n = 4096;
    const int64_t rot = 1365;
    const int64_t total = 18000000;
    const int64_t modulus = 1000000007;

    int64_t *nums = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t p = 0; p < n; p++) {
        nums[p] = 2 * ((p + rot) % n);
    }

    int64_t span = 2 * n;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t target = k % span;
        int64_t idx = search(nums, n, target);
        acc = (acc + idx + 2) % modulus;
    }

    free(nums);
    printf("%lld\n", (long long)acc);
    return 0;
}

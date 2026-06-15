/* LeetCode #31 bench — C (mirror of next_permutation.kara).
 *
 * Canonical four-move next-permutation, enumerating all K! permutations REPEAT
 * times and folding a rolling checksum. The no-allocation floor: the array lives
 * on the stack and the permutation is stepped in place.
 */
#include <stdio.h>
#include <stdint.h>

static void next_permutation(int64_t *nums, int len) {
    int i = len - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) {
        i--;
    }
    if (i >= 0) {
        int j = len - 1;
        while (nums[j] <= nums[i]) {
            j--;
        }
        int64_t tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
    int lo = i + 1;
    int hi = len - 1;
    while (lo < hi) {
        int64_t t = nums[lo];
        nums[lo] = nums[hi];
        nums[hi] = t;
        lo++;
        hi--;
    }
}

int main(void) {
    const int k = 10;
    const int64_t fact = 3628800; /* 10! */
    const int64_t repeat = 8;
    const int64_t modulus = 2147483647; /* 2^31 - 1 */

    int64_t nums[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    int64_t acc = 0;

    for (int64_t r = 0; r < repeat; r++) {
        for (int64_t step = 0; step < fact; step++) {
            int64_t h = 0;
            for (int i = 0; i < k; i++) {
                h = (h * 131 + nums[i]) % modulus;
            }
            acc = (acc + h) % modulus;
            next_permutation(nums, k);
        }
    }

    printf("%lld\n", (long long)acc);
    return 0;
}

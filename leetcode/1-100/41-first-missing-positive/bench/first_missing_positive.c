// LeetCode #41 bench mirror — C, the in-place cyclic-sort solver (★).
//
// Mirrors bench/first_missing_positive.kara: swap each in-range value to its home index
// v-1, then scan for the first slot not holding its home value. The buffer is allocated
// once and overwritten in place each iteration. Same workload (TOTAL refills of a k-rotated
// permutation with a punched gap) and the same answer-fold checksum as every other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t first_missing_positive(int64_t *nums, int64_t n) {
    int64_t i = 0;
    while (i < n) {
        int64_t v = nums[i];
        if (v >= 1 && v <= n && nums[v - 1] != v) {
            int64_t t = nums[v - 1];
            nums[v - 1] = v;
            nums[i] = t;
        } else {
            i++;
        }
    }
    for (int64_t j = 0; j < n; j++) {
        if (nums[j] != j + 1) {
            return j + 1;
        }
    }
    return n + 1;
}

int main(void) {
    const int64_t total = 200000;
    const int64_t n = 100;
    const int64_t modulus = 1000000007;

    int64_t *nums = (int64_t *)malloc((size_t)n * sizeof(int64_t));

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t rot = k % n;
        for (int64_t i = 0; i < n; i++) {
            nums[i] = ((i + rot) % n) + 1;
        }
        nums[k % n] = n + 7;

        int64_t ans = first_missing_positive(nums, n);
        acc = (acc * 131 + ans) % modulus;
    }

    free(nums);
    printf("%lld\n", (long long)acc);
    return 0;
}

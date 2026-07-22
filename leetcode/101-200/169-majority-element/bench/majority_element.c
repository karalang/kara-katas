/* LeetCode 169 — Majority Element benchmark kernel (C mirror, clang -O3).
 *
 * Build-once + punch: LCG-filled N values with a 60% majority, Boyer-Moore scan
 * run K times with a one-element perturbation each round. Sink = sum of the K
 * results. Identical algorithm to the Kāra / Rust / Go / Python mirrors. */
#include <stdio.h>
#include <stdlib.h>

static long majority_element(const long *nums, long n) {
    long candidate = nums[0];
    long count = 0;
    for (long i = 0; i < n; i++) {
        long x = nums[i];
        if (count == 0) candidate = x;
        if (x == candidate) count++;
        else count--;
    }
    return candidate;
}

int main(void) {
    const long n = 10000000, k = 20, majority = 7;
    long *nums = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) % 2147483648L;
        if (state % 100 < 60) nums[i] = majority;
        else nums[i] = state % 1000000 + 1000;
    }
    long sink = 0;
    for (long round = 0; round < k; round++) {
        long idx = (round * 7919L) % n;
        nums[idx] = nums[idx] + 1;
        sink += majority_element(nums, n);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}

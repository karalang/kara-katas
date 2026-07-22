/* LeetCode 164 — Maximum Gap benchmark kernel (C mirror, clang -O3).
 *
 * Build-once + punch: LCG-filled N values, maximum_gap called K times with a
 * one-element perturbation each round. Sink = sum of the K gaps. Identical
 * algorithm to the Kāra / Rust / Go / Python mirrors. */
#include <stdio.h>
#include <stdlib.h>

static long maximum_gap(const long *nums, long n) {
    if (n < 2) return 0;
    long lo = nums[0], hi = nums[0];
    for (long i = 1; i < n; i++) {
        if (nums[i] < lo) lo = nums[i];
        if (nums[i] > hi) hi = nums[i];
    }
    if (lo == hi) return 0;

    long bsize = (hi - lo) / (n - 1);
    if (bsize < 1) bsize = 1;
    long bcount = (hi - lo) / bsize + 1;

    char *used = calloc((size_t)bcount, sizeof(char));
    long *bmin = malloc((size_t)bcount * sizeof(long));
    long *bmax = malloc((size_t)bcount * sizeof(long));

    for (long i = 0; i < n; i++) {
        long x = nums[i];
        long idx = (x - lo) / bsize;
        if (used[idx]) {
            if (x < bmin[idx]) bmin[idx] = x;
            if (x > bmax[idx]) bmax[idx] = x;
        } else {
            bmin[idx] = bmax[idx] = x;
            used[idx] = 1;
        }
    }

    long gap = 0, prev_max = lo;
    for (long b = 0; b < bcount; b++) {
        if (used[b]) {
            if (bmin[b] - prev_max > gap) gap = bmin[b] - prev_max;
            prev_max = bmax[b];
        }
    }
    free(used);
    free(bmin);
    free(bmax);
    return gap;
}

int main(void) {
    const long n = 1000000, k = 30, range = 1000000000;
    long *nums = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) % 2147483648L;
        nums[i] = state % range;
    }
    long sink = 0;
    for (long round = 0; round < k; round++) {
        long idx = (round * 7919L) % n;
        nums[idx] = (nums[idx] + 1 + round) % range;
        sink += maximum_gap(nums, n);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #209 — Minimum Size Subarray Sum.
//
// Build-once + punch: one large positive-integer array is generated once with a
// deterministic LCG, then the O(n) sliding-window `min_subarray_len` is run for
// TARGETS distinct thresholds. The window's inner shrink loop is data-dependent
// (it runs a variable number of times per step, gated on the running sum), so the
// scan does NOT vectorize. Sink = sum of the answers over all targets.

static long min_subarray_len(long target, const long *nums, long n) {
    long left = 0, sum = 0, best = -1;
    for (long right = 0; right < n; right++) {
        sum += nums[right];
        while (sum >= target) {
            long len = right - left + 1;
            if (best == -1 || len < best) best = len;
            sum -= nums[left];
            left++;
        }
    }
    return best == -1 ? 0 : best;
}

int main(void) {
    long n = 200000;
    long targets = 290;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nums[i] = 1 + state % 100; // 1..100, all positive
    }

    long sink = 0;
    for (long t = 0; t < targets; t++) {
        long target = 200 + t * 80;
        sink += min_subarray_len(target, nums, n);
    }

    printf("%ld\n", sink);
    free(nums);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #213 — House Robber II.
//
// Build-once + punch: one large positive-value array is generated once with a
// deterministic LCG, then the circular House Robber DP is run over WINDOWS
// different sub-windows of it (a fresh start offset each time). Each rob() is two
// linear O(1)-space DP passes whose `cur = max(prev + v, cur)` recurrence is
// loop-carried (this step depends on the last), so it does NOT vectorize. Sink =
// sum of the max take over all windows.

static long rob_linear(const long *nums, long lo, long hi) {
    long prev = 0, cur = 0;
    for (long i = lo; i < hi; i++) {
        long take = prev + nums[i];
        long next = take > cur ? take : cur;
        prev = cur;
        cur = next;
    }
    return cur;
}

static long rob_window(const long *nums, long s, long w) {
    if (w == 1) return nums[s];
    long skip_last = rob_linear(nums, s, s + w - 1);
    long skip_first = rob_linear(nums, s + 1, s + w);
    return skip_last > skip_first ? skip_last : skip_first;
}

int main(void) {
    long n = 100000;
    long window = 2000;
    long windows = 130000;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nums[i] = 1 + state % 1000; // 1..1000, all positive
    }

    long span = n - window;
    long sink = 0;
    for (long w = 0; w < windows; w++) {
        long s = (w * 977) % span;
        sink += rob_window(nums, s, window);
    }

    printf("%ld\n", sink);
    free(nums);
    return 0;
}

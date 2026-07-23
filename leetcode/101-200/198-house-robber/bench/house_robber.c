#include <stdio.h>
#include <stdlib.h>

static long max_i64(long a, long b) { return a > b ? a : b; }

static long rob(const long *nums, long n) {
    long prev2 = 0;
    long prev = 0;
    for (long i = 0; i < n; i++) {
        long cur = max_i64(prev, prev2 + nums[i]);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}

int main(void) {
    long n = 5000;
    long passes = 90000;

    long *nums = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long b = 0; b < n; b++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        nums[b] = (state >> 16) % 1000;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long idx = state % n;
        nums[idx] = (state >> 16) % 1000;
        sink += rob(nums, n);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}

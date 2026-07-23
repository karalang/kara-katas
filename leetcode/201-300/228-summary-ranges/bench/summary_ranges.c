#include <stdio.h>
#include <stdlib.h>

static long summary_metric(const long *nums, long n) {
    long i = 1;
    long start = nums[0];
    long ranges = 0;
    long esum = 0;
    while (i <= n) {
        if (i == n || nums[i] != nums[i - 1] + 1) {
            long end = nums[i - 1];
            ranges += 1;
            esum += start + end;
            if (i < n) start = nums[i];
        }
        i += 1;
    }
    return ranges + esum;
}

int main(void) {
    long n = 1000000;
    long passes = 250;

    long *nums = malloc(n * sizeof(long));
    long state = 12345;
    long v = 0;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        v = v + 1 + (state % 3);
        nums[c] = v;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        sink += summary_metric(nums, n);
    }
    printf("%ld\n", sink);
    free(nums);
    return 0;
}

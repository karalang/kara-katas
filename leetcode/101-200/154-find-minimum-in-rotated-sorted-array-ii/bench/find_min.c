#include <stdio.h>
#include <stdlib.h>

static long find_min(const long *nums, long n) {
    long lo = 0, hi = n - 1;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) lo = mid + 1;
        else if (nums[mid] < nums[hi]) hi = mid;
        else hi = hi - 1;
    }
    return nums[lo];
}

int main(void) {
    long n = 2000, punches = 75000;
    long *arr = malloc(n * sizeof(long));
    for (long z = 0; z < n; z++) arr[z] = 0;

    long state = 12345;
    long sink = 0;
    for (long pn = 0; pn < punches; pn++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long start = state % 1000000;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long rot = state % n;

        long cur = start;
        for (long k = 0; k < n; k++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long inc = (state % 5 == 0) ? (state / 5) % 4 : 0;
            cur = cur + inc;
            arr[(k + rot) % n] = cur;
        }

        sink += find_min(arr, n);
    }
    printf("%ld\n", sink);
    free(arr);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

static long find_peak(const long *arr, long lo, long hi) {
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        if (arr[mid] < arr[mid + 1]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int main(void) {
    long n = 4000000, window = 4096, passes = 1000000;
    long *arr = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        arr[c] = state % 1000003;
    }
    long span = n - window;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long base = (p * 4099L) % span;
        arr[base] = (arr[base] + 1) % 1000003;
        sink += find_peak(arr, base, base + window - 1);
    }
    printf("%ld\n", sink);
    free(arr);
    return 0;
}

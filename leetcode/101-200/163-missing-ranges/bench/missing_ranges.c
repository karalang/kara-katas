#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long count;
    long checksum;
} Res;

static Res missing_ranges(const long *arr, long start, long len, long lower, long upper) {
    long count = 0, checksum = 0;
    long prev = lower - 1;
    for (long i = 0; i <= len; i++) {
        long cur = (i < len) ? arr[start + i] : upper + 1;
        if (cur - prev >= 2) {
            count++;
            checksum += (prev + 1) + (cur - 1);
        }
        prev = cur;
    }
    Res r = {count, checksum};
    return r;
}

int main(void) {
    long n = 1000000, window = 2000, passes = 120000;
    long *arr = malloc(n * sizeof(long));
    long state = 12345, val = 0;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val += 1 + (state % 3);
        arr[c] = val;
    }
    long span = n - window;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long start = (p * 7919L) % span;
        long lower = arr[start];
        long upper = arr[start + window - 1] + (p % 5);
        Res r = missing_ranges(arr, start, window, lower, upper);
        sink += r.count + r.checksum;
    }
    printf("%ld\n", sink);
    free(arr);
    return 0;
}

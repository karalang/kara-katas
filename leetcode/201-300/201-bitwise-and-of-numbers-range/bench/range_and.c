#include <stdio.h>

static long range_and(long left, long right) {
    long lo = left, hi = right, shift = 0;
    while (lo < hi) {
        lo >>= 1;
        hi >>= 1;
        shift++;
    }
    return lo << shift;
}

int main(void) {
    long iters = 20000000;
    long state = 12345;
    long sink = 0;
    for (long it = 0; it < iters; it++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long x = state;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long y = state;
        long lo = x < y ? x : y;
        long hi = x < y ? y : x;
        sink += range_and(lo, hi);
    }
    printf("%ld\n", sink);
    return 0;
}

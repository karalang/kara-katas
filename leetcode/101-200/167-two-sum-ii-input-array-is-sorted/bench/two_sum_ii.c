#include <stdio.h>
#include <stdlib.h>

static void two_sum(const long *arr, long n, long target, long *out) {
    long lo = 0, hi = n - 1;
    while (lo < hi) {
        long sum = arr[lo] + arr[hi];
        if (sum == target) {
            out[0] = lo + 1;
            out[1] = hi + 1;
            return;
        }
        if (sum < target) {
            lo++;
        } else {
            hi--;
        }
    }
    out[0] = -1;
    out[1] = -1;
}

int main(void) {
    long n = 20000, passes = 20000;
    long *arr = malloc(n * sizeof(long));
    long state = 12345, val = 0;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val += 1 + (state % 3);
        arr[c] = val;
    }
    long sink = 0;
    long out[2];
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long a = state % n;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long b = state % n;
        if (a == b) b = (a + 1) % n;
        long target = arr[a] + arr[b];
        two_sum(arr, n, target, out);
        sink += out[0] + out[1];
    }
    printf("%ld\n", sink);
    free(arr);
    return 0;
}

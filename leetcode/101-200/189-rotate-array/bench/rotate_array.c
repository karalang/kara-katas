#include <stdio.h>
#include <stdlib.h>

static void reverse_range(long *a, long lo, long hi) {
    long i = lo;
    long j = hi;
    while (i < j) {
        long t = a[i];
        a[i] = a[j];
        a[j] = t;
        i++;
        j--;
    }
}

static void rotate(long *a, long n, long k) {
    if (n == 0) {
        return;
    }
    long kk = k % n;
    reverse_range(a, 0, n - 1);
    reverse_range(a, 0, kk - 1);
    reverse_range(a, kk, n - 1);
}

static long checksum(const long *a, long n) {
    long chk = 0;
    for (long i = 0; i < n; i++) {
        chk = ((chk * 131) + a[i]) & 2147483647;
    }
    return chk;
}

int main(void) {
    long n = 30000;
    long passes = 4000;

    long *a = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long b = 0; b < n; b++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        a[b] = state;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long k = state % n;
        rotate(a, n, k);
        sink += checksum(a, n);
    }
    printf("%ld\n", sink);
    free(a);
    return 0;
}

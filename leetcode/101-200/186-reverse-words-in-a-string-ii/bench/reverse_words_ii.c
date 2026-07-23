#include <stdio.h>
#include <stdlib.h>

static void reverse_range(long *a, long lo, long hi) {
    long i = lo, j = hi;
    while (i < j) {
        long t = a[i];
        a[i] = a[j];
        a[j] = t;
        i++;
        j--;
    }
}

static void reverse_words(long *a, long n) {
    if (n > 0) reverse_range(a, 0, n - 1);
    long start = 0;
    for (long i = 0; i <= n; i++) {
        if (i == n || a[i] == 32) {
            if (i > start) reverse_range(a, start, i - 1);
            start = i + 1;
        }
    }
}

int main(void) {
    long target_len = 30000, passes = 3000;
    long cap = target_len + 16;
    long *buf = malloc(cap * sizeof(long));
    long n = 0;
    long state = 12345;
    int first = 1;
    while (n < target_len) {
        if (first) {
            first = 0;
        } else {
            buf[n++] = 32;
        }
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long wlen = 1 + (state % 8);
        for (long w = 0; w < wlen; w++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            buf[n++] = 97 + (state % 26);
        }
    }

    long modv = 1000000007;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 131 + 7) % n;
        if (buf[idx] != 32) {
            buf[idx] = 97 + (((buf[idx] - 97) + 1) % 26);
        }
        reverse_words(buf, n);
        long cs = 0;
        for (long k = 0; k < n; k++) {
            cs = (cs * 131 + buf[k]) % modv;
        }
        sink += cs;
    }
    printf("%ld\n", sink);
    free(buf);
    return 0;
}

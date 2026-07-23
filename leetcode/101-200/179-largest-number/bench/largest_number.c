#include <stdio.h>
#include <stdlib.h>

static long num_digits(long x) {
    long d = 1;
    long t = x;
    while (t >= 10) { d++; t /= 10; }
    return d;
}

static long pow10(long k) {
    long r = 1;
    for (long i = 0; i < k; i++) r *= 10;
    return r;
}

static long concat_val(long a, long b) {
    return a * pow10(num_digits(b)) + b;
}

static void sort_desc(long *arr, long n) {
    for (long i = 1; i < n; i++) {
        long j = i;
        while (j > 0 && concat_val(arr[j - 1], arr[j]) < concat_val(arr[j], arr[j - 1])) {
            long tmp = arr[j - 1];
            arr[j - 1] = arr[j];
            arr[j] = tmp;
            j--;
        }
    }
}

static long checksum(const long *arr, long n) {
    long modv = 1000000007;
    long cs = 0;
    for (long i = 0; i < n; i++) {
        long x = arr[i];
        long p = pow10(num_digits(x) - 1);
        while (p > 0) {
            long d = (x / p) % 10;
            cs = (cs * 10 + d) % modv;
            p /= 10;
        }
    }
    return cs;
}

int main(void) {
    long n = 500, passes = 400;
    long *base = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        base[c] = state % 1000;
    }
    long *arr = malloc(n * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        for (long k = 0; k < n; k++) arr[k] = base[k];
        long idx = p % n;
        arr[idx] = (arr[idx] + p + 1) % 1000;
        sort_desc(arr, n);
        sink += checksum(arr, n);
    }
    printf("%ld\n", sink);
    free(base); free(arr);
    return 0;
}

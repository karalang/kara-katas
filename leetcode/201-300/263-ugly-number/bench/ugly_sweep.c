// Benchmark workload for LeetCode #263 — Ugly Number (C mirror).
// Mirrors ugly_sweep.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdint.h>

static long gcd_(long a, long b) {
    long x = a, y = b;
    while (y != 0) {
        long t = x % y;
        x = y;
        y = t;
    }
    return x;
}

static int is_ugly(long n) {
    if (n <= 0) return 0;
    long m = n;
    long g = gcd_(m, 30);
    while (g > 1) {
        m /= g;
        g = gcd_(m, 30);
    }
    return m == 1;
}

int main(void) {
    long n = 10000000;
    long limit = INT64_MAX;

    long ring[64];
    long rs = 7717;
    for (long k = 0; k < 64; k++) {
        long v = 1;
        for (long steps = 0; steps < 40; steps++) {
            rs = (rs * 1103515245L + 12345L) & 2147483647L;
            long pick = (rs / 65536L) % 3;
            long f = (pick == 1) ? 3 : ((pick == 2) ? 5 : 2);
            if (v <= limit / f) v *= f;
            else steps = 40;
        }
        ring[k] = v;
    }

    long state = 263263, uglies = 0, digest = 0;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long hi = state;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long probe = hi * 2147483648L + state;
        if (i % 512 == 0) probe = ring[(i / 512) % 64];
        long bit = 0;
        if (is_ugly(probe)) { uglies++; bit = 1; }
        digest = (digest * 131 + bit * 7 + probe % 1000003L) % 1000000007L;
    }

    printf("%ld\n%ld\n", uglies, digest);
    return 0;
}

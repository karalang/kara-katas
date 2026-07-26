/* Benchmark harness for LeetCode #260 — Single Number III.
 * Mirrors single_number_iii.kara algorithm-for-algorithm. */

#include <stdio.h>

#define NP 4
#define K 100000
#define ITERS 2600
#define N (2 * K + 2)

static void two_singles(const long long *nums, long long n, long long *out) {
    long long x = 0;
    for (long long i = 0; i < n; i++) {
        x ^= nums[i];
    }
    long long bit = x & (0 - x);

    long long a = 0;
    long long b = 0;
    for (long long j = 0; j < n; j++) {
        if ((nums[j] & bit) != 0) {
            a ^= nums[j];
        } else {
            b ^= nums[j];
        }
    }
    if (a <= b) {
        out[0] = a;
        out[1] = b;
    } else {
        out[0] = b;
        out[1] = a;
    }
}

int main(void) {
    static long long arrays[NP][N];

    for (long long p = 0; p < NP; p++) {
        static long long vals[K];
        long long x = p + 1;
        for (long long t = 0; t < K; t++) {
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            vals[t] = (x / 65536LL) % 100000LL;
        }
        long long e = 0;
        for (int pass = 0; pass < 2; pass++) {
            for (long long q = 0; q < K; q++) {
                arrays[p][e++] = vals[q];
            }
        }
        arrays[p][e++] = 999983LL + p;
        arrays[p][e++] = 1000003LL + p;
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        long long r[2];
        two_singles(arrays[idx], N, r);
        sink = (sink * 31 + r[0] + r[1] * 7) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

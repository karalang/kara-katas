/* Benchmark harness for LeetCode #137 — Single Number II.
 * Mirrors single_number.kara algorithm-for-algorithm. */

#include <stdio.h>
#include <stdlib.h>

#define NP 4
#define K 30000
#define ITERS 40
#define N (3 * K + 1)

static long long mask32(void) {
    return 4294967295LL;
}

static long long sign_extend32(long long v) {
    if (v >= 2147483648LL) {
        return v - 4294967296LL;
    }
    return v;
}

static long long single_ones_twos(const long long *nums, long long n) {
    long long mask = mask32();
    long long ones = 0;
    long long twos = 0;
    for (long long i = 0; i < n; i++) {
        long long x = nums[i] & mask;
        ones = (ones ^ x) & (~twos) & mask;
        twos = (twos ^ x) & (~ones) & mask;
    }
    return sign_extend32(ones);
}

static long long single_bitcount(const long long *nums, long long n) {
    long long res = 0;
    for (long long b = 0; b < 32; b++) {
        long long cnt = 0;
        for (long long i = 0; i < n; i++) {
            if (((nums[i] >> b) & 1LL) == 1LL) {
                cnt++;
            }
        }
        if ((cnt % 3) != 0) {
            res |= 1LL << b;
        }
    }
    return sign_extend32(res);
}

int main(void) {
    static long long arrays[NP][N];

    for (long long j = 0; j < NP; j++) {
        static long long vals[K];
        long long x = j + 1;
        for (long long t = 0; t < K; t++) {
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            long long hi = x / 65536LL;
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            vals[t] = (hi * 32768LL + x / 65536LL) % 100000LL;
        }
        long long e = 0;
        for (long long pass = 0; pass < 3; pass++) {
            for (long long q = 0; q < K; q++) {
                arrays[j][e++] = vals[q];
            }
        }
        arrays[j][e++] = 999983LL + j;
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        long long a = single_ones_twos(arrays[idx], N);
        long long b = single_bitcount(arrays[idx], N);
        if (a != b) {
            sink += 1000000000LL;
        }
        sink = (sink + a + b) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

/* Benchmark harness for LeetCode #238 — Product of Array Except Self.
 * Mirrors product_except_self.kara algorithm-for-algorithm.
 *
 * `%` on a negative left operand truncates toward zero in C, matching Kara,
 * Rust and Go. Python floors instead, so the Python mirror applies an explicit
 * truncating mod to agree — see product_except_self.py.
 */

#include <stdio.h>

#define NP 8
#define N 100000
#define ITERS 400

static long long arrays[NP][N];
static long long out[N];

static void product_except_self(const long long *nums, long long n) {
    long long prefix = 1;
    for (long long i = 0; i < n; i++) {
        out[i] = prefix;
        prefix *= nums[i];
    }

    long long suffix = 1;
    for (long long j = n - 1; j >= 0; j--) {
        out[j] *= suffix;
        suffix *= nums[j];
    }
}

static void lcg_vals(long long seed, long long n, long long *dst) {
    long long x = seed;
    for (long long t = 0; t < n; t++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        dst[t] = 1 - 2 * ((x / 65536) % 2);
    }
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        lcg_vals(j + 1, N, arrays[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        product_except_self(arrays[idx], N);
        for (long long v = 0; v < N; v++) {
            sink = (sink + (v + 1) * out[v]) % 1000000007LL;
        }
    }
    printf("%lld\n", sink);
    return 0;
}

/* Benchmark harness for LeetCode #268 — Missing Number.
 * Mirrors missing_number.kara algorithm-for-algorithm. */

#include <stdio.h>
#include <stdlib.h>

#define NP 4
#define N 1000000L
#define ITERS 850

static long long missing_number(const long long *nums, long long n) {
    long long acc = n;
    for (long long i = 0; i < n; i++) {
        acc = acc ^ i ^ nums[i];
    }
    return acc;
}

int main(void) {
    long long *arrays[NP];

    for (long long p = 0; p < NP; p++) {
        long long missing = 200000 * p + 137;

        arrays[p] = malloc(sizeof(long long) * (size_t)N);
        for (long long z = 0; z < N; z++) {
            arrays[p][z] = 0;
        }
        long long v = 0;
        for (long long t = 0; t < N; t++) {
            if (v == missing) {
                v++;
            }
            long long idx = (t * 499979L) % N;
            arrays[p][idx] = v;
            v++;
        }
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink * 31 + missing_number(arrays[idx], N)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

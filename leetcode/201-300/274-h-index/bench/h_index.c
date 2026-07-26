/* Benchmark harness for LeetCode #274 — H-Index.
 * Mirrors h_index.kara algorithm-for-algorithm.
 *
 * The sort is each language's stdlib sort. For C that means qsort, whose
 * per-comparison indirect call is a real and well-known handicap against
 * Rust's/Go's monomorphised pdqsort and Kara's monomorphised sort — see
 * ../README.md § Benchmarks, which measures that handicap rather than
 * hiding it. */

#include <stdio.h>
#include <stdlib.h>

#define NP 4
#define N 60000L
#define ITERS 600

static int cmp_ll(const void *a, const void *b) {
    long long x = *(const long long *)a;
    long long y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long h_index(const long long *cit, long long n) {
    long long *v = malloc(sizeof(long long) * (size_t)n);
    for (long long i = 0; i < n; i++) {
        v[i] = cit[i];
    }
    qsort(v, (size_t)n, sizeof(long long), cmp_ll);
    long long r = 0;
    for (long long j = 0; j < n; j++) {
        if (v[j] >= n - j) {
            r = n - j;
            break;
        }
    }
    free(v);
    return r;
}

int main(void) {
    long long *arrays[NP];

    for (long long p = 0; p < NP; p++) {
        arrays[p] = malloc(sizeof(long long) * (size_t)N);
        long long x = p + 1;
        for (long long t = 0; t < N; t++) {
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            long long r = (x / 65536LL) % 32768LL;
            if (p == 0) {
                arrays[p][t] = r % 30000;
            } else if (p == 1) {
                arrays[p][t] = r % 40;
            } else if (p == 2) {
                arrays[p][t] = (r % 7) * 3000;
            } else {
                arrays[p][t] = t + (r % 5);
            }
        }
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink * 31 + h_index(arrays[idx], N)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

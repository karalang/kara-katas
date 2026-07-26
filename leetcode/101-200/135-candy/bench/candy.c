/* Benchmark harness for LeetCode #135 — Candy.
 * Mirrors candy.kara algorithm-for-algorithm, including the explicit
 * descending index loop for the right-to-left pass.
 */

#include <stdio.h>

#define NP 8
#define N 200000
#define ITERS 150

static long long arrays[NP][N];
static long long c[N];

static long long candy(const long long *ratings, long long n) {
    if (n == 0) {
        return 0;
    }
    for (long long k = 0; k < n; k++) {
        c[k] = 1;
    }

    for (long long i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1]) {
            c[i] = c[i - 1] + 1;
        }
    }

    for (long long i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i + 1] && c[i] <= c[i + 1]) {
            c[i] = c[i + 1] + 1;
        }
    }

    long long total = 0;
    for (long long i = 0; i < n; i++) {
        total += c[i];
    }
    return total;
}

static void lcg(long long seed, long long n, long long cap, long long *dst) {
    long long x = seed;
    for (long long k = 0; k < n; k++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        dst[k] = (x / 65536) % cap;
    }
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        lcg(j + 1, N, (j % 2 == 0) ? 4 : 100000, arrays[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink + candy(arrays[idx], N)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

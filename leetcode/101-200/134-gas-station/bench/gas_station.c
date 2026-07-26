/* Benchmark harness for LeetCode #134 — Gas Station.
 * Mirrors gas_station.kara algorithm-for-algorithm.
 */

#include <stdio.h>

#define NP 8
#define N 200000
#define ITERS 1200

static long long gases[NP][N];
static long long costs[NP][N];

static long long can_complete(const long long *gas, const long long *cost, long long n) {
    long long total = 0;
    long long tank = 0;
    long long start = 0;
    for (long long i = 0; i < n; i++) {
        long long d = gas[i] - cost[i];
        total += d;
        tank += d;
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }
    return total >= 0 ? start : -1;
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
        lcg(j + 1, N, 100, gases[j]);
        lcg(j + 100, N, (j % 2 == 0) ? 90 : 110, costs[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink + can_complete(gases[idx], costs[idx], N)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

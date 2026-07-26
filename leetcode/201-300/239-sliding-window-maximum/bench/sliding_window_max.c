/* Benchmark harness for LeetCode #239 — Sliding Window Maximum.
 * Mirrors sliding_window_max.kara algorithm-for-algorithm, including the
 * array-plus-head-cursor deque (not a ring buffer), so the data structure
 * matches the other four.
 */

#include <stdio.h>

#define NP 8
#define N 50000
#define CAPV 100000
#define K 64
#define ITERS 300

static long long arrays[NP][N];
static long long dq[N];
static long long out[N];

static long long max_sliding_window(const long long *nums, long long n, long long k) {
    long long dqn = 0;
    long long head = 0;
    long long outn = 0;

    for (long long i = 0; i < n; i++) {
        while (dqn > head) {
            long long back = dq[dqn - 1];
            if (nums[back] <= nums[i]) {
                dqn--;
            } else {
                break;
            }
        }
        dq[dqn++] = i;

        if (dq[head] <= i - k) {
            head++;
        }

        if (i >= k - 1) {
            out[outn++] = nums[dq[head]];
        }
    }
    return outn;
}

static void lcg(long long seed, long long n, long long cap, long long *dst) {
    long long x = seed;
    for (long long t = 0; t < n; t++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        dst[t] = x % cap;
    }
}

int main(void) {
    for (long long j = 0; j < NP; j++) {
        lcg(j + 1, N, CAPV, arrays[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        long long m = max_sliding_window(arrays[idx], N, K);
        for (long long v = 0; v < m; v++) {
            sink = (sink + (v + 1) * out[v]) % 1000000007LL;
        }
    }
    printf("%lld\n", sink);
    return 0;
}

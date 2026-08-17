/* Benchmark harness for LeetCode #287 — Find the Duplicate Number.
 * Mirrors find_duplicate.kara algorithm-for-algorithm. */

#include <stdio.h>
#include <stdlib.h>

#define NP 4
#define N 200000L
#define ITERS 80

static long long find_duplicate(const long long *nums) {
    long long slow = nums[0];
    long long fast = nums[0];
    slow = nums[slow];
    fast = nums[nums[fast]];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[nums[fast]];
    }
    long long finder = nums[0];
    while (finder != slow) {
        finder = nums[finder];
        slow = nums[slow];
    }
    return finder;
}

int main(void) {
    long long *arrays[NP];

    for (long long p = 0; p < NP; p++) {
        long long *order = malloc(sizeof(long long) * (size_t)N);
        for (long long v = 1; v <= N; v++) {
            order[v - 1] = v;
        }
        long long x = p + 12345;
        for (long long k = N - 1; k > 0; k--) {
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            long long wd0 = x / 65536LL;
            x = (x * 1103515245LL + 12345LL) % 2147483648LL;
            long long j = (wd0 * 32768LL + x / 65536LL) % (k + 1);
            long long tmp = order[k];
            order[k] = order[j];
            order[j] = tmp;
        }

        arrays[p] = malloc(sizeof(long long) * (size_t)(N + 1));
        for (long long z = 0; z <= N; z++) {
            arrays[p][z] = 0;
        }
        for (long long t = 0; t < N; t++) {
            long long nxt = (t + 1) % N;
            arrays[p][order[t]] = order[nxt];
        }
        arrays[p][0] = order[p * 37];
        free(order);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink * 31 + find_duplicate(arrays[idx])) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

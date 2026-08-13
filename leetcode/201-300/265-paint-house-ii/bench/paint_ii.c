// Benchmark workload for LeetCode #265 — Paint House II (C mirror).
// Mirrors paint_ii.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n = 4000, k = 32, rounds = 1300;
    long inf = 1000000000000L;

    long *cost = malloc(n * k * sizeof(long));
    long state = 265265;
    for (long z = 0; z < n * k; z++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        cost[z] = (state / 65536L) % 40 + 1;
    }

    long *prev = calloc(k, sizeof(long));
    long *cur = calloc(k, sizeof(long));

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        long start = (r * 7919L) % n;

        for (long c = 0; c < k; c++) prev[c] = cost[start * k + c];

        for (long i = 1; i < n; i++) {
            long min1 = inf, idx1 = -1, min2 = inf;
            for (long j = 0; j < k; j++) {
                long v = prev[j];
                if (v < min1) { min2 = min1; min1 = v; idx1 = j; }
                else if (v < min2) { min2 = v; }
            }

            long row = ((start + i) % n) * k;
            for (long t = 0; t < k; t++) {
                long best = (t == idx1) ? min2 : min1;
                cur[t] = cost[row + t] + best;
            }

            long *tmp = prev; prev = cur; cur = tmp;
        }

        long answer = inf, fold = 0;
        for (long p = 0; p < k; p++) {
            long v = prev[p];
            if (v < answer) answer = v;
            fold = (fold * 31 + v) % 1000000007L;
        }
        sink = (sink * 131 + answer + fold) % 1000000007L;
    }

    printf("%ld\n", sink);
    free(cost); free(prev); free(cur);
    return 0;
}

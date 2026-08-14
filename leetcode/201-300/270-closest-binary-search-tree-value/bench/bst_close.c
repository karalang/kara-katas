// Benchmark workload for LeetCode #270 — Closest BST Value (C mirror).
// Mirrors bst_close.kara algorithm-for-algorithm, including the hand-written
// native absolute value (see that file for why hand-writing it was wrong).
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(void) {
    long n = 30000, queries = 100000, rounds = 22;

    long *val = malloc(n * sizeof(long));
    long *left = malloc(n * sizeof(long));
    long *right = malloc(n * sizeof(long));
    long cnt = 0, state = 270270;

    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long hi = state / 65536L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long v = (hi * 32768L + state / 65536L) % 1000000L;
        if (cnt == 0) {
            val[cnt] = v; left[cnt] = -1; right[cnt] = -1; cnt++;
        } else {
            long cur = 0;
            for (;;) {
                if (v < val[cur]) {
                    if (left[cur] < 0) {
                        val[cnt] = v; left[cnt] = -1; right[cnt] = -1; cnt++;
                        left[cur] = cnt - 1;
                        break;
                    }
                    cur = left[cur];
                } else {
                    if (right[cur] < 0) {
                        val[cnt] = v; left[cnt] = -1; right[cnt] = -1; cnt++;
                        right[cur] = cnt - 1;
                        break;
                    }
                    cur = right[cur];
                }
            }
        }
    }

    double *targets = malloc(queries * sizeof(double));
    for (long q = 0; q < queries; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long th = state / 65536L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long whole = (th * 32768L + state / 65536L) % 1100000L - 50000L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        double frac = (double)((state / 65536L) % 1000L) / 1000.0;
        targets[q] = (double)whole + frac;
    }

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        for (long t = 0; t < queries; t++) {
            double target = targets[t];
            long best = val[0];
            double best_diff = fabs((double)val[0] - target);
            long cur = 0;
            while (cur >= 0) {
                long v = val[cur];
                double d = fabs((double)v - target);
                if (d < best_diff || (d == best_diff && v < best)) {
                    best = v; best_diff = d;
                }
                cur = ((double)v < target) ? right[cur] : left[cur];
            }
            sink = (sink * 31 + best) % 1000000007L;
        }
    }
    printf("%ld\n", sink);
    free(val); free(left); free(right); free(targets);
    return 0;
}

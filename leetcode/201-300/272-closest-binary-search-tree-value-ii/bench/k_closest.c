/* Benchmark workload for LeetCode #272 — Closest Binary Search Tree Value II.
 *
 * Algorithm-for-algorithm mirror of k_closest.kara. See that file's header for
 * what this lane measures and for the three parity decisions (hoisted stacks,
 * each language's own absolute value, targets that span the value range). */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    const int64_t node_count = 30000;
    const int64_t target_count = 100000;
    const int64_t k = 8;
    const int64_t rounds = 10;
    const int64_t span = 1000000;

    int64_t *val = malloc((size_t)node_count * sizeof(int64_t));
    int64_t *left = malloc((size_t)node_count * sizeof(int64_t));
    int64_t *right = malloc((size_t)node_count * sizeof(int64_t));
    int64_t n = 0;
    int64_t state = 272272;
    int64_t placed = 0, tries = 0;
    while (placed < node_count && tries < node_count * 4) {
        state = (state * 1103515245 + 12345) & 2147483647;
        int64_t v = (state / 256) % span;
        tries++;
        if (n == 0) {
            val[n] = v; left[n] = -1; right[n] = -1; n++;
            placed++;
        } else {
            int64_t cur = 0;
            int dup = 0, done = 0;
            while (!done) {
                if (v == val[cur]) {
                    dup = 1; done = 1;
                } else if (v < val[cur]) {
                    if (left[cur] < 0) {
                        val[n] = v; left[n] = -1; right[n] = -1; n++;
                        left[cur] = n - 1;
                        done = 1;
                    } else { cur = left[cur]; }
                } else {
                    if (right[cur] < 0) {
                        val[n] = v; left[n] = -1; right[n] = -1; n++;
                        right[cur] = n - 1;
                        done = 1;
                    } else { cur = right[cur]; }
                }
            }
            if (!dup) placed++;
        }
    }

    double *targets = malloc((size_t)target_count * sizeof(double));
    double tmin = 0.0, tmax = 0.0;
    for (int64_t t = 0; t < target_count; t++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        int64_t whole = (state / 256) % span;
        state = (state * 1103515245 + 12345) & 2147483647;
        double frac = (double)((state / 256) % 1000) / 1000.0;
        double x = (double)whole + frac;
        if (t == 0) { tmin = x; tmax = x; }
        if (x < tmin) tmin = x;
        if (x > tmax) tmax = x;
        targets[t] = x;
    }

    const int64_t depth_cap = 256;
    int64_t *pred = calloc((size_t)depth_cap, sizeof(int64_t));
    int64_t *succ = calloc((size_t)depth_cap, sizeof(int64_t));
    int64_t *lower = calloc((size_t)k, sizeof(int64_t));
    int64_t *upper = calloc((size_t)k, sizeof(int64_t));
    int64_t *outv = calloc((size_t)k, sizeof(int64_t));

    int64_t sink = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t q = 0; q < target_count; q++) {
            double target = targets[q];

            int64_t pt = 0, st = 0, cur = 0;
            while (cur >= 0) {
                if ((double)val[cur] < target) {
                    pred[pt++] = cur;
                    cur = right[cur];
                } else {
                    succ[st++] = cur;
                    cur = left[cur];
                }
            }

            int64_t nl = 0, nu = 0, taken = 0;
            while (taken < k && (pt > 0 || st > 0)) {
                int take_pred = pt > 0;
                if (pt > 0 && st > 0) {
                    double dp = fabs((double)val[pred[pt - 1]] - target);
                    double ds = fabs((double)val[succ[st - 1]] - target);
                    take_pred = dp <= ds;
                }
                if (take_pred) {
                    int64_t node = pred[--pt];
                    int64_t c = left[node];
                    while (c >= 0) { pred[pt++] = c; c = right[c]; }
                    lower[nl++] = val[node];
                } else {
                    int64_t node = succ[--st];
                    int64_t c = right[node];
                    while (c >= 0) { succ[st++] = c; c = left[c]; }
                    upper[nu++] = val[node];
                }
                taken++;
            }

            int64_t w = 0;
            for (int64_t i = nl - 1; i >= 0; i--) outv[w++] = lower[i];
            for (int64_t j = 0; j < nu; j++) outv[w++] = upper[j];

            int64_t acc = 0;
            for (int64_t p = 0; p < w; p++) acc = (acc * 31 + outv[p]) % 1000000007;
            sink = (sink * 131 + acc) % 1000000007;
        }
    }

    int64_t vlo = val[0], vhi = val[0];
    for (int64_t m = 1; m < n; m++) {
        if (val[m] < vlo) vlo = val[m];
        if (val[m] > vhi) vhi = val[m];
    }
    printf("%lld\n", (long long)sink);
    printf("nodes %lld values %lld..%lld targets %lld..%lld\n",
           (long long)n, (long long)vlo, (long long)vhi,
           (long long)tmin, (long long)tmax);

    free(val); free(left); free(right); free(targets);
    free(pred); free(succ); free(lower); free(upper); free(outv);
    return 0;
}

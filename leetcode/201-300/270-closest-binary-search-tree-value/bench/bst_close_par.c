// Benchmark workload for LeetCode #270 — Closest BST Value (C mirror).
// Mirrors bst_close.kara algorithm-for-algorithm, including the hand-written
// native absolute value (see that file for why hand-writing it was wrong).
#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* One contiguous slice of the query stream per worker, each with a private
 * partial. The tree and target arrays are read-only, so nothing is shared to
 * race on; the partials live in the thread-argument structs rather than in a
 * shared array, so there is no false sharing either. */
typedef struct {
    const long *val, *left, *right;
    const double *targets;
    long queries, from, to, partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    long acc = 0;
    for (long t = w->from; t < w->to; t++) {
        double target = w->targets[t % w->queries];
        long best = w->val[0];
        double best_diff = fabs((double)w->val[0] - target);
        long cur = 0;
        while (cur >= 0) {
            long v = w->val[cur];
            double d = fabs((double)v - target);
            if (d < best_diff || (d == best_diff && v < best)) { best = v; best_diff = d; }
            cur = ((double)v < target) ? w->right[cur] : w->left[cur];
        }
        acc = (acc + (t * 1000003L + best) % 1000000007L) % 1000000007L;
    }
    w->partial = acc;
    return NULL;
}

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

    const long total = (long)queries * rounds;
    long ncpu = sysconf(_SC_NPROCESSORS_ONLN);
    if (ncpu < 1) ncpu = 1;
    int nthreads = (int)ncpu;
    pthread_t *tids = malloc((size_t)nthreads * sizeof(pthread_t));
    Work *work = malloc((size_t)nthreads * sizeof(Work));
    long chunk = (total + nthreads - 1) / nthreads;
    for (int i = 0; i < nthreads; i++) {
        long from = chunk * i, to = from + chunk;
        if (to > total) to = total;
        if (from > total) from = total;
        work[i] = (Work){val, left, right, targets, queries, from, to, 0};
        pthread_create(&tids[i], NULL, worker, &work[i]);
    }
    long sink = 0;
    for (int i = 0; i < nthreads; i++) {
        pthread_join(tids[i], NULL);
        sink = (sink + work[i].partial) % 1000000007L;
    }
    printf("%ld\n", sink);
    printf("queries %ld nodes %ld\n", total, cnt);
    free(val); free(left); free(right); free(targets);
    return 0;
}

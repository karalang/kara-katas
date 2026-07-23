#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #215 — Kth Largest Element in an Array.
 *
 * Quickselect's Lomuto partition, run once on a fixed array, is a converging-
 * pointer kernel an optimizer can partly erase. The honest scale workload runs
 * quickselect PASSES times, and REBUILDS the array from the shared PRNG stream
 * every pass — the input differs each pass (the stream never repeats), so the
 * work cannot be hoisted, and the data-dependent swaps stay real. A fixed
 * last-element pivot keeps it deterministic; the k-th largest value is unique
 * regardless of pivot choice, so every language agrees. Sink = sum of the k-th
 * largest values over all passes. */

#define N       120000L   /* array length per pass          */
#define PASSES  420L      /* number of quickselect runs      */
#define K       40000L    /* k-th largest (fixed)            */

static long partition(long *a, long lo, long hi) {
    long pivot = a[hi];
    long i = lo;
    for (long j = lo; j < hi; j++) {
        if (a[j] < pivot) {
            long t = a[i]; a[i] = a[j]; a[j] = t;
            i += 1;
        }
    }
    long t = a[i]; a[i] = a[hi]; a[hi] = t;
    return i;
}

static long quickselect(long *a, long lo, long hi, long target) {
    if (lo == hi) return a[lo];
    long p = partition(a, lo, hi);
    if (p == target) return a[p];
    if (target < p) return quickselect(a, lo, p - 1, target);
    return quickselect(a, p + 1, hi, target);
}

int main(void) {
    long *a = malloc(N * sizeof(long));
    long state = 12345;
    long target = N - K;   /* ascending index of the K-th largest */
    long sink = 0;
    for (long p = 0; p < PASSES; p++) {
        for (long i = 0; i < N; i++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            a[i] = state;
        }
        sink += quickselect(a, 0, N - 1, target);
    }
    printf("%ld\n", sink);
    free(a);
    return 0;
}

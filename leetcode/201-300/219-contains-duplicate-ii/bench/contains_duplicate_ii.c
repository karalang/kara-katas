#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #219 — Contains Duplicate II.
 *
 * The kata's kernel is a value->last-index hash map: as it scans, a value whose
 * previous index is within window k is a "nearby duplicate". One boolean query
 * short-circuits on the first hit, so it cannot sustain a benchmark. The bench
 * keeps the identical map kernel but runs it as a full sweep that COUNTS nearby
 * duplicates, over every window width k in 1..KMAX, on ONE big PRNG array. Every
 * k forces a full value->index scan (real map throughput, no early-exit erosion);
 * the per-element get+insert with a data-dependent gap branch does not vectorize.
 * Sink = total nearby-duplicate hits summed over all k. (Same scaling spirit as
 * #216 counting combinations instead of listing them.)
 *
 * C mirrors the language maps with an open-addressing table (key + last index +
 * per-run generation stamp), cleared in O(1) per k with no memset refill. */

#define N      1000000L    /* array length                          */
#define KMAX   40L         /* sweep k = 1..KMAX                      */
#define M      49999L      /* value range (0..M-1); prime, breaks LCG lattice */
#define CAP    (1L << 17)  /* table capacity (pow2 > M)             */

static long keys[CAP];
static long idxs[CAP];
static long stamp[CAP];

static long count_nearby(const long *a, long k, long gen) {
    long hits = 0;
    for (long i = 0; i < N; i++) {
        long x = a[i];
        long h = ((unsigned long)(x * 2654435761UL)) & (CAP - 1);
        while (stamp[h] == gen) {
            if (keys[h] == x) {
                if (i - idxs[h] <= k) hits += 1;
                idxs[h] = i;               /* keep only the latest index */
                goto next;
            }
            h = (h + 1) & (CAP - 1);
        }
        stamp[h] = gen; keys[h] = x; idxs[h] = i;
    next:;
    }
    return hits;
}

int main(void) {
    long *a = malloc(N * sizeof(long));
    long state = 12345;
    for (long i = 0; i < N; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        a[i] = state % M;
    }

    long sink = 0;
    for (long k = 1; k <= KMAX; k++) {
        sink += count_nearby(a, k, k);    /* gen = k (>= 1, never 0) */
    }
    printf("%ld\n", sink);
    free(a);
    return 0;
}

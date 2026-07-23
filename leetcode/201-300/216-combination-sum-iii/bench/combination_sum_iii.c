#include <stdio.h>

/* Benchmark workload for LeetCode #216 — Combination Sum III.
 *
 * The kata backtracks over ascending digits 1..9 to list every combination of
 * exactly k distinct digits summing to n. One (k,n) query is tiny. The bench
 * scales it two ways: it COUNTS combinations instead of materializing them, and
 * it widens the digit pool to 1..D so the search tree is large, then sums the
 * count over a whole grid of (k,n) pairs. The recursion's ascending-digit prune
 * (`d > remaining => stop`) is data-dependent branching that does not vectorize.
 * This kernel is exhaustive enumeration, so it needs no PRNG — it is identical
 * across all five languages by construction. Sink = total combinations summed
 * over the (k,n) grid. */

#define D      36L    /* digit pool is 1..D            */
#define KMAX   6L     /* combination sizes 1..KMAX     */
#define NMAX   150L   /* target sums 1..NMAX           */

static long count_combos(long start, long k, long remaining) {
    if (k == 0) return remaining == 0 ? 1 : 0;
    long total = 0;
    for (long d = start; d <= D; d++) {
        if (d > remaining) break;   /* ascending digits: no later d fits */
        total += count_combos(d + 1, k - 1, remaining - d);
    }
    return total;
}

int main(void) {
    long sink = 0;
    for (long k = 1; k <= KMAX; k++) {
        for (long n = 1; n <= NMAX; n++) {
            sink += count_combos(1, k, n);
        }
    }
    printf("%ld\n", sink);
    return 0;
}

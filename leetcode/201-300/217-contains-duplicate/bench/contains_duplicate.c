#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #217 — Contains Duplicate.
 *
 * The kata scans an array once through a hash set, returning true the first time
 * a value repeats. The bench builds ONE big PRNG array, then slides a fixed-width
 * window across it and runs contains_duplicate on every window, counting how many
 * windows contain a duplicate. Each window drives a fresh hash-set membership
 * test whose early-exit is a data-dependent branch (does not vectorize); the load
 * is dominated by hash probing, which is the point — this kata measures the set.
 * Sink = number of windows that contain a duplicate.
 *
 * C mirrors the language sets with an open-addressing table cleared in O(1) via a
 * per-window generation stamp (no memset refill of the measured kernel). */

#define BIG   240000L      /* base array length                     */
#define W     800L        /* window width                          */
#define M     2000000L    /* value range (0..M-1)                  */
#define CAP   2048L       /* table capacity (pow2 >= 2*W)          */

static long keys[CAP];
static long stamp[CAP];

/* returns 1 if the window base[w..w+W] has a repeated value, else 0 */
static int window_has_dup(const long *base, long w, long gen) {
    for (long t = 0; t < W; t++) {
        long x = base[w + t];
        long h = ((unsigned long)(x * 2654435761UL)) & (CAP - 1);
        while (stamp[h] == gen) {
            if (keys[h] == x) return 1;      /* already seen => duplicate */
            h = (h + 1) & (CAP - 1);
        }
        stamp[h] = gen;
        keys[h] = x;
    }
    return 0;
}

int main(void) {
    long *base = malloc(BIG * sizeof(long));
    long state = 12345;
    for (long i = 0; i < BIG; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        base[i] = state % M;
    }

    long windows = BIG - W;
    long sink = 0;
    for (long w = 0; w < windows; w++) {
        sink += window_has_dup(base, w, w + 1);   /* gen = w+1 (never 0) */
    }
    printf("%ld\n", sink);
    free(base);
    return 0;
}

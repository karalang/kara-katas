#include <stdio.h>
#include <stdlib.h>

/* Copy-list-with-random-pointer (index-pool deep copy) as an allocate + pointer-
 * chase kernel.
 *
 * Build-once + punch: one big list of N nodes (a linear `next` chain plus a
 * `random` edge per node targeting any node or -1 for null) is generated once
 * with a deterministic 32-bit LCG (overflow-safe in i64; values from the HIGH
 * bits to dodge the LCG's short-period low bits). The list is deep-copied K
 * times; before each copy one node's `random` target is repointed (the punch)
 * so the structure — and its checksum — changes every pass and the optimizer
 * cannot hoist. The copy resolves `next`/`random` through an explicit old->new
 * map (a flat array; the index pool makes the map natural). Sink = running total
 * of a checksum over each copy's (val, next-index, random-index) structure. */

int main(void) {
    long n = 3000, k = 40000;
    long *oval = malloc(n * sizeof(long));
    long *onext = malloc(n * sizeof(long));
    long *ornd = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        oval[i] = (state >> 16) % 1000;
        onext[i] = (i + 1 < n) ? (i + 1) : -1;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long r = state >> 16;
        ornd[i] = (r % 4 == 0) ? -1 : (r % n); /* ~25% null randoms */
    }

    /* old->new map + the copy's flat node arrays (reused per pass). */
    long *map = malloc(n * sizeof(long));
    long *nval = malloc(n * sizeof(long));
    long *nnext = malloc(n * sizeof(long));
    long *nrnd = malloc(n * sizeof(long));

    long sink = 0;
    for (long p = 0; p < k; p++) {
        long ii = p % n;
        ornd[ii] = (p * 37 + 11) % n; /* punch: repoint one random edge */

        for (long i = 0; i < n; i++) { nval[i] = oval[i]; map[i] = i; } /* clone + map */
        for (long i = 0; i < n; i++) {
            nnext[i] = (onext[i] == -1) ? -1 : map[onext[i]];
            nrnd[i] = (ornd[i] == -1) ? -1 : map[ornd[i]];
        }
        long checksum = 0;
        for (long i = 0; i < n; i++) {
            checksum += nval[i] + nnext[i] * 7 + nrnd[i] * 13;
        }
        sink += checksum;
    }
    printf("%ld\n", sink);
    free(oval); free(onext); free(ornd);
    free(map); free(nval); free(nnext); free(nrnd);
    return 0;
}

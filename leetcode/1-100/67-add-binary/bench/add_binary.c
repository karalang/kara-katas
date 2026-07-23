#include <stdio.h>
#include <stdlib.h>

/* Add-binary (two-pointer column add) as a carry-ripple kernel.
 *
 * Build-once + punch: one big 0/1 bit buffer is generated with a deterministic
 * 32-bit LCG (overflow-safe in i64; bits taken from the HIGH bits to dodge the
 * LCG's short-period low bits). Each pass adds two fixed-width windows of that
 * buffer column-by-column from the least-significant end, rippling a carry — a
 * loop-carried dependency that does NOT vectorize. A single-bit punch before
 * each add keeps the optimizer from hoisting. Sink = running total of the
 * popcount (set-bit count, carry-out included) of every column-add result. */

#define W 96

static long add_popcount(const long *bits, long off_a, long off_b) {
    long carry = 0, pop = 0;
    for (long k = W - 1; k >= 0; k--) {
        long sum = carry + bits[off_a + k] + bits[off_b + k];
        pop += sum & 1;      /* emitted bit */
        carry = sum >> 1;    /* ripples left */
    }
    pop += carry;            /* final carry-out */
    return pop;
}

int main(void) {
    long bn = 2000000, passes = 2600000;
    long *bits = malloc(bn * sizeof(long));
    long state = 12345;
    for (long c = 0; c < bn; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        bits[c] = (state >> 16) & 1;
    }
    long span = bn - W;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 101 + 7) % bn;
        bits[idx] = 1 - bits[idx];          /* punch */
        long off_a = (p * 37) % span;
        long off_b = (p * 53 + 17) % span;
        sink += add_popcount(bits, off_a, off_b);
    }
    printf("%ld\n", sink);
    free(bits);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

/* Length-of-last-word (reverse scan) as a throughput kernel.
 *
 * Build-once + punch: a large letters+spaces buffer is generated once with a
 * deterministic 32-bit LCG (overflow-safe in i64; values taken from the high
 * bits to dodge the LCG's short-period low bits), then the last-word scan is
 * run over PASSES different end positions, each preceded by a single-cell flip
 * so the optimizer cannot hoist the repeated computation. The scan is two
 * data-dependent while loops (skip trailing spaces, then count the run) — a
 * genuine non-vectorizable scalar kernel. Sink = sum of the last-word lengths. */

static long last_word_len(const long *buf, long end) {
    long i = end;
    while (i >= 0 && buf[i] == 32) i--;      /* skip trailing spaces */
    long len = 0;
    while (i >= 0 && buf[i] != 32) { len++; i--; } /* count the run */
    return len;
}

int main(void) {
    long n = 4000000, passes = 6500000;
    long *buf = malloc(n * sizeof(long));
    long state = 12345;
    for (long c = 0; c < n; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long r = state >> 16;
        buf[c] = (r % 100 < 18) ? 32 : (65 + r % 26); /* ~18% spaces */
    }
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 97 + 13) % n;
        buf[idx] = (buf[idx] == 32) ? (65 + p % 26) : 32; /* punch */
        long e = (p * 89 + 41) % n;
        sink += last_word_len(buf, e);
    }
    printf("%ld\n", sink);
    free(buf);
    return 0;
}

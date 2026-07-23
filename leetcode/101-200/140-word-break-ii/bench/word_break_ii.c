#include <stdio.h>
#include <stdlib.h>

// Exponential-backtracking segmentation COUNT for LeetCode #140. Short strings /
// small dicts keep the search tractable; counts are bounded by compositions of
// SLEN (≈10^4) so the sink never overflows. The dict SET is a flat stamped
// base-A table (hand-rolled; see word_break_ii.kara header and #139).
static long alpha = 3, minlen = 1, maxlen = 3, slen = 16;
static long *s;
static char *table;
static long base[8];

static long count(long start) {
    if (start == slen) return 1;
    long total = 0, code = 0;
    for (long end = start + 1; end <= slen && end - start <= maxlen; end++) {
        code = code * alpha + s[end - 1];
        long ln = end - start;
        if (ln >= minlen) {
            if (table[base[ln] + code]) total += count(end);
        }
    }
    return total;
}

int main(void) {
    long dwords = 25;
    long cases = 80000;

    base[0] = 0;
    base[1] = 0;
    long pwr = alpha, acc = 0;
    for (long b = 2; b <= maxlen; b++) {
        acc += pwr;
        base[b] = acc;
        pwr *= alpha;
    }
    long tsize = acc + pwr;

    table = malloc((size_t)tsize);
    s = malloc((size_t)slen * sizeof(long));

    long state = 12345;
    long sink = 0;

    for (long c = 0; c < cases; c++) {
        for (long z = 0; z < tsize; z++) table[z] = 0;
        for (long i = 0; i < slen; i++) {
            state = (state * 1103515245 + 12345) & 2147483647;
            long r = state >> 16;
            s[i] = r % alpha;
        }
        for (long w = 0; w < dwords; w++) {
            state = (state * 1103515245 + 12345) & 2147483647;
            long rl = state >> 16;
            long span = maxlen - minlen + 1;
            long wlen = minlen + (rl % span);
            long code = 0;
            for (long k = 0; k < wlen; k++) {
                state = (state * 1103515245 + 12345) & 2147483647;
                long rc = state >> 16;
                code = code * alpha + (rc % alpha);
            }
            table[base[wlen] + code] = 1;
        }

        sink += count(0);
    }

    printf("%ld\n", sink);
    return 0;
}

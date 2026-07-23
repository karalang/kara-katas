#include <stdio.h>
#include <stdlib.h>

// Build-once + punch word-break. The dictionary is a SET; C hand-rolls it as a
// flat stamped bool table indexed by a per-length base-A word key (mirrors the
// Set[String] in the Kāra kata; see word_break.kara header).
int main(void) {
    long alpha = 5;
    long maxlen = 4;
    long n = 5000;
    long dwords = 120;
    long win = 24;
    long windows = 2200000;

    long base[8];
    base[0] = 0;
    base[1] = 0;
    long pwr = alpha;
    long acc = 0;
    for (long b = 2; b <= maxlen; b++) {
        acc += pwr;
        base[b] = acc;
        pwr *= alpha;
    }
    long tsize = acc + pwr;

    char *table = calloc((size_t)tsize, 1);

    long state = 12345;

    long *s = malloc((size_t)n * sizeof(long));
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long r = state >> 16;
        s[i] = r % alpha;
    }

    for (long w = 0; w < dwords; w++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long rl = state >> 16;
        long wlen = 2 + (rl % (maxlen - 1));
        long code = 0;
        for (long k = 0; k < wlen; k++) {
            state = (state * 1103515245 + 12345) & 2147483647;
            long rc = state >> 16;
            long ch = rc % alpha;
            code = code * alpha + ch;
        }
        long key = base[wlen] + code;
        table[key] = 1;
    }

    char *dp = malloc((size_t)(win + 1));

    long sink = 0;
    for (long wnd = 0; wnd < windows; wnd++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long ro = state >> 16;
        long off = ro % (n - win);

        for (long z = 0; z <= win; z++) dp[z] = 0;
        dp[0] = 1;

        for (long ii = 1; ii <= win; ii++) {
            long low = 0;
            if (ii > maxlen) low = ii - maxlen;
            long code = 0;
            long pw = 1;
            long ln = 0;
            for (long j = ii - 1; j >= low; j--) {
                long ch = s[off + j];
                code = ch * pw + code;
                pw *= alpha;
                ln++;
                if (dp[j]) {
                    long key = base[ln] + code;
                    if (table[key]) {
                        dp[ii] = 1;
                        break;
                    }
                }
            }
        }

        if (dp[win]) sink += off + 1;
    }

    printf("%ld\n", sink);
    return 0;
}

#include <stdio.h>
#include <stdlib.h>

/* Benchmark workload for LeetCode #214 — Shortest Palindrome.
 *
 * The kata's core is the KMP prefix-function over comb = s + '#' + reverse(s);
 * fail[last] is the longest-palindromic-prefix (lps) length. One call is O(n).
 * The bench turns it into a throughput kernel: build ONE big symbol string over
 * a tiny alphabet (so palindromic prefixes actually occur and lps varies), then
 * slide a fixed-width window across it and, for every window, build comb and run
 * the prefix-function, summing lps. The prefix-function's `len = fail[len-1]`
 * fallback is a loop-carried, data-dependent recurrence — it does NOT vectorize.
 * Sink = sum of lps over all windows.  Symbols are i64 codes (alphabet 0..A-1),
 * with -1 as the '#' separator, so all five languages run the identical kernel. */

#define BIG    260000L   /* length of the base symbol string          */
#define W      512L      /* window width                               */
#define ALPHA  2L        /* alphabet size (small => rich palindromes)  */

int main(void) {
    long *base = malloc(BIG * sizeof(long));
    long state = 12345;
    for (long i = 0; i < BIG; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        base[i] = state % ALPHA;
    }

    long m = 2 * W + 1;                 /* comb length: W + 1 + W */
    long *comb = malloc(m * sizeof(long));
    long *fail = malloc(m * sizeof(long));

    long windows = BIG - W;             /* stride 1 sliding windows */
    long sink = 0;
    for (long w = 0; w < windows; w++) {
        /* comb = base[w..w+W] + '#' + reverse(base[w..w+W]) */
        for (long i = 0; i < W; i++) comb[i] = base[w + i];
        comb[W] = -1;
        for (long i = 0; i < W; i++) comb[W + 1 + i] = base[w + W - 1 - i];

        fail[0] = 0;
        long len = 0;
        long idx = 1;
        while (idx < m) {
            if (comb[idx] == comb[len]) {
                len += 1;
                fail[idx] = len;
                idx += 1;
            } else if (len > 0) {
                len = fail[len - 1];
            } else {
                fail[idx] = 0;
                idx += 1;
            }
        }
        sink += fail[m - 1];
    }

    printf("%ld\n", sink);
    free(base); free(comb); free(fail);
    return 0;
}

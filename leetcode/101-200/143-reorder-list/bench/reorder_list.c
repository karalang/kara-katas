#include <stdio.h>
#include <stdlib.h>

// Build-once + punch reorder-list over an index pool (see reorder_list.kara).
// Each pass generates the interleaved order, rewires nxt, and walks it, folding a
// position-weighted checksum into the sink.
int main(void) {
    long n = 100000;
    long k = 1000;
    long valmod = 1000;

    long *vals = malloc((size_t)n * sizeof(long));
    long *nxt = malloc((size_t)n * sizeof(long));
    long *order = malloc((size_t)n * sizeof(long));

    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        vals[i] = (state >> 16) % valmod;
    }

    long sink = 0;
    for (long p = 0; p < k; p++) {
        long pi = p % n;
        vals[pi] = (vals[pi] + 1) % valmod;

        long lo = 0, hi = n - 1, idx = 0;
        int take_lo = 1;
        while (lo <= hi) {
            if (take_lo) { order[idx] = lo; lo++; }
            else { order[idx] = hi; hi--; }
            take_lo = !take_lo;
            idx++;
        }

        for (long r = 0; r + 1 < n; r++) nxt[order[r]] = order[r + 1];
        nxt[order[n - 1]] = -1;

        long cur = order[0], pos = 0;
        while (cur >= 0) {
            long w = (pos % 997) + 1;
            sink += w * vals[cur];
            pos++;
            cur = nxt[cur];
        }
    }

    printf("%ld\n", sink);
    return 0;
}

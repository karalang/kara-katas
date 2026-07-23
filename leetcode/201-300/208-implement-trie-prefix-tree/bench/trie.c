#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #208 — Implement Trie (Prefix Tree).
//
// Build-once + punch: a trie is built ONCE from NWORDS deterministic PRNG words
// over a small alphabet (index-pool representation — all nodes in one flat array,
// children keyed by letter), then NQUERY PRNG query words are walked against it.
// Each walk is a data-dependent pointer chase `cur = children[cur*ALPHA + c]`
// (a loop-carried dependent load that does NOT vectorize). Sink accumulates a
// weighted count of prefix hits and exact-word hits.

#define ALPHA 5

int main(void) {
    long nwords = 30000;
    long nquery = 8000000;

    long cap = 4;
    long *children = malloc(cap * ALPHA * sizeof(long));
    long *is_end = malloc(cap * sizeof(long));
    for (long a = 0; a < ALPHA; a++) children[0 * ALPHA + a] = 0;
    is_end[0] = 0;
    long nnodes = 1; // root at index 0

    long state = 12345;

    // Build phase.
    for (long w = 0; w < nwords; w++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long len = 2 + state % 7;
        long cur = 0;
        for (long k = 0; k < len; k++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long c = state % ALPHA;
            long nxt = children[cur * ALPHA + c];
            if (nxt == 0) {
                if (nnodes == cap) {
                    cap *= 2;
                    children = realloc(children, cap * ALPHA * sizeof(long));
                    is_end = realloc(is_end, cap * sizeof(long));
                }
                long idx = nnodes++;
                for (long a = 0; a < ALPHA; a++) children[idx * ALPHA + a] = 0;
                is_end[idx] = 0;
                children[cur * ALPHA + c] = idx;
                cur = idx;
            } else {
                cur = nxt;
            }
        }
        is_end[cur] = 1;
    }

    // Query phase.
    long sink = 0;
    for (long q = 0; q < nquery; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long len = 2 + state % 7;
        long cur = 0;
        long alive = 1;
        for (long k = 0; k < len; k++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long c = state % ALPHA;
            if (alive) {
                long nxt = children[cur * ALPHA + c];
                if (nxt == 0) {
                    alive = 0;
                } else {
                    cur = nxt;
                }
            }
        }
        if (alive) {
            sink += 1;
            if (is_end[cur] == 1) sink += 2;
        }
    }

    printf("%ld\n", sink);
    free(children);
    free(is_end);
    return 0;
}

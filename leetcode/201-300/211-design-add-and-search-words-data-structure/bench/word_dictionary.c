#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #211 — Add and Search Words Data Structure.
//
// Build-once + punch: an index-pool trie is built ONCE from NWORDS deterministic
// PRNG words (fixed length WLEN over a small alphabet), then NQUERY PRNG patterns
// — each carrying a sprinkling of '.' wildcards — are matched by the recursive
// backtracking DFS that is this problem's whole point (a literal follows one
// edge; a '.' fans out to every child). The trie is deliberately sized so only a
// fraction of patterns match, keeping the sink discriminating. The recursion's
// data-dependent branching does NOT vectorize. Sink = count of matching patterns.

#define ALPHA 6
#define WLEN 6

static long *children;
static long *is_end;

static int dfs(const long *wild, const long *letter, long cur, long pos) {
    if (pos == WLEN) return is_end[cur] == 1;
    if (wild[pos]) {
        for (long a = 0; a < ALPHA; a++) {
            long nc = children[cur * ALPHA + a];
            if (nc != 0 && dfs(wild, letter, nc, pos + 1)) return 1;
        }
        return 0;
    }
    long nc = children[cur * ALPHA + letter[pos]];
    if (nc == 0) return 0;
    return dfs(wild, letter, nc, pos + 1);
}

int main(void) {
    long nwords = 20000;
    long nquery = 8000000;

    long cap = 4;
    children = malloc(cap * ALPHA * sizeof(long));
    is_end = malloc(cap * sizeof(long));
    for (long a = 0; a < ALPHA; a++) children[a] = 0;
    is_end[0] = 0;
    long nnodes = 1;

    long state = 12345;

    // Build phase.
    for (long w = 0; w < nwords; w++) {
        long cur = 0;
        for (long k = 0; k < WLEN; k++) {
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
    long wild[WLEN];
    long letter[WLEN];
    long sink = 0;
    for (long q = 0; q < nquery; q++) {
        for (long k = 0; k < WLEN; k++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long v = state;
            wild[k] = (v % 6 == 0) ? 1 : 0; // ~1 wildcard per pattern on average
            letter[k] = (v / 6) % ALPHA;
        }
        if (dfs(wild, letter, 0, 0)) sink += 1;
    }

    printf("%ld\n", sink);
    free(children);
    free(is_end);
    return 0;
}

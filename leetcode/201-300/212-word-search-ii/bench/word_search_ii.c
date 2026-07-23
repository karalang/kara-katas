#include <stdio.h>
#include <stdlib.h>

// Benchmark workload for LeetCode #212 — Word Search II.
//
// Build-once + fresh input: the word trie (index-pool) is built ONCE from NWORDS
// PRNG words over a small alphabet, then the trie-guided board DFS is run RUNS
// times, each over a FRESH SIZE x SIZE board drawn from the ongoing PRNG stream —
// so every run is a genuinely distinct search that cannot be hoisted. Word-end
// flags are restored before each run (the DFS clears each on collection, the real
// Word Search II "collect once" semantics). The DFS is a backtracking grid walk
// in lockstep with the trie — dead trie edges prune whole branches, a
// data-dependent traversal that does NOT vectorize. The sink checksums every trie
// node the walk descends into (plus each collected word's identity), so it
// reflects the actual board-dependent traversal, not just the near-invariant
// count of completed words. Sink = accumulated traversal checksum over all runs.

#define ALPHA 6
#define SIZE 12
#define CELLS (SIZE * SIZE)

static long dfs(long *board, const long *children, long *is_end, long r, long c, long node) {
    long cell = board[r * SIZE + c];
    if (cell == -1) return 0;             // already on the path
    long nxt = children[node * ALPHA + cell];
    if (nxt == 0) return 0;               // no trie edge -> prune
    long cnt = nxt;                       // checksum every node the walk descends into
    if (is_end[nxt] == 1) {
        is_end[nxt] = 0;                  // collect each word once per run
        cnt += nxt;                       // + collected-word identity
    }
    board[r * SIZE + c] = -1;             // mark visited
    if (r > 0) cnt += dfs(board, children, is_end, r - 1, c, nxt);
    if (r + 1 < SIZE) cnt += dfs(board, children, is_end, r + 1, c, nxt);
    if (c > 0) cnt += dfs(board, children, is_end, r, c - 1, nxt);
    if (c + 1 < SIZE) cnt += dfs(board, children, is_end, r, c + 1, nxt);
    board[r * SIZE + c] = cell;           // restore
    return cnt;
}

int main(void) {
    long nwords = 4000;
    long runs = 40000;

    long cap = 4;
    long *children = malloc(cap * ALPHA * sizeof(long));
    long *is_end0 = malloc(cap * sizeof(long));
    for (long a = 0; a < ALPHA; a++) children[a] = 0;
    is_end0[0] = 0;
    long nnodes = 1;

    long state = 12345;

    // Build trie once.
    for (long w = 0; w < nwords; w++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long len = 5 + state % 4; // 5..8
        long cur = 0;
        for (long k = 0; k < len; k++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long ch = state % ALPHA;
            long nxt = children[cur * ALPHA + ch];
            if (nxt == 0) {
                if (nnodes == cap) {
                    cap *= 2;
                    children = realloc(children, cap * ALPHA * sizeof(long));
                    is_end0 = realloc(is_end0, cap * sizeof(long));
                }
                long idx = nnodes++;
                for (long a = 0; a < ALPHA; a++) children[idx * ALPHA + a] = 0;
                is_end0[idx] = 0;
                children[cur * ALPHA + ch] = idx;
                cur = idx;
            } else {
                cur = nxt;
            }
        }
        is_end0[cur] = 1;
    }

    // Build board once.
    long *board = malloc(CELLS * sizeof(long));
    long *is_end = malloc(nnodes * sizeof(long));

    long sink = 0;
    for (long run = 0; run < runs; run++) {
        for (long i = 0; i < nnodes; i++) is_end[i] = is_end0[i];
        // Fresh board each run from the ongoing PRNG stream: every run is a
        // genuinely distinct search, so the found set (and the sink) truly
        // varies and the DFS cannot be hoisted.
        for (long i = 0; i < CELLS; i++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            board[i] = state % ALPHA;
        }
        long found = 0;
        for (long r = 0; r < SIZE; r++) {
            for (long c = 0; c < SIZE; c++) {
                found += dfs(board, children, is_end, r, c, 0);
            }
        }
        sink += found;
    }

    printf("%ld\n", sink);
    free(children);
    free(is_end0);
    free(board);
    free(is_end);
    return 0;
}

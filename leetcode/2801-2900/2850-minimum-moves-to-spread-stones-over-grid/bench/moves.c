// LeetCode #2850: Minimum Moves to Spread Stones Over Grid -- the
// bench: the ★ arm over every grid of nine stones, 24310 of them, all
// made first, then each answered 5 times. The spare stones and empty
// cells go in fixed arrays of 9, as the vectors of the other languages
// hold at most 8.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t r, c; } Cell;

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t spread(int64_t k, const Cell *from, int64_t nfrom, const Cell *to, int64_t nto, bool *used) {
    if (k == nfrom) return 0;
    int64_t best = INT64_MAX;
    for (int64_t j = 0; j < nto; j++) {
        if (!used[j]) {
            used[j] = true;
            int64_t d = abs64(from[k].r - to[j].r) + abs64(from[k].c - to[j].c) + spread(k + 1, from, nfrom, to, nto, used);
            if (d < best) best = d;
            used[j] = false;
        }
    }
    return best;
}

static int64_t minimum_moves(const int64_t *grid) {
    Cell from[9], to[9];
    int64_t nfrom = 0, nto = 0;
    for (int64_t r = 0; r < 3; r++) {
        for (int64_t c = 0; c < 3; c++) {
            int64_t k = grid[r * 3 + c];
            if (k == 0) to[nto++] = (Cell){r, c};
            for (int64_t i = 1; i < k; i++) from[nfrom++] = (Cell){r, c};
        }
    }
    bool used[9] = {false};
    return spread(0, from, nfrom, to, nto, used);
}

static int64_t *grids;
static int64_t ngrids;

static void every(int cell, int64_t left, int64_t *counts) {
    if (cell == 8) {
        counts[8] = left;
        for (int i = 0; i < 9; i++) grids[ngrids * 9 + i] = counts[i];
        ngrids++;
        return;
    }
    for (int64_t k = 0; k <= left; k++) {
        counts[cell] = k;
        every(cell + 1, left - k, counts);
    }
}

int main(void) {
    const int64_t rounds = 5;
    grids = malloc(sizeof(int64_t) * 9 * 24310);
    int64_t counts[9] = {0};
    every(0, 9, counts);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < ngrids; g++) {
            int64_t moves = minimum_moves(grids + g * 9);
            total += moves;
            check = (check * 31 + moves + r) % 1000000007;
        }
    }
    printf("%lld grids, %lld rounds: %lld moves, checksum %lld\n", (long long)ngrids, (long long)rounds, (long long)total, (long long)check);
    free(grids);
    return 0;
}

/*
 * Benchmark workload — Word Search (LeetCode #79).
 * C mirror of bench/word_search.kara. Enumerates every self-avoiding walk (up to
 * `depth` steps) from every start cell of a fixed all-'A' 5x5 board and folds each
 * visited cell into a threaded accumulator — the 4-neighbour, in-place mark/restore
 * DFS backtracking that powers word search, with the letter-match replaced by
 * "any unvisited cell, up to depth" so every branch is taken. K=12 iterations seeded
 * by the iteration index. The DFS recursion is the measured work. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define ROWS 5
#define COLS 5

/* Nested heap board (uint8_t **, one malloc'd row per line) — the same pointer-chased
 * layout Kara's Vec[Vec[u8]] uses, so the comparison measures the DFS on an equal data
 * structure rather than a fixed 2D stack array's locality advantage. */
static int64_t walk(uint8_t **board, int64_t r, int64_t c, int64_t depth,
                    int64_t acc) {
    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return acc;
    if (board[r][c] == 0) return acc;
    int64_t a = (acc * 131 + (r * COLS + c) + 1) % 1000000007;
    if (depth == 0) return a;
    uint8_t saved = board[r][c];
    board[r][c] = 0;
    a = walk(board, r + 1, c, depth - 1, a);
    a = walk(board, r - 1, c, depth - 1, a);
    a = walk(board, r, c + 1, depth - 1, a);
    a = walk(board, r, c - 1, depth - 1, a);
    board[r][c] = saved;
    return a;
}

static int64_t search_all(uint8_t **board, int64_t depth, int64_t seed) {
    int64_t a = seed;
    for (int64_t r = 0; r < ROWS; r++)
        for (int64_t c = 0; c < COLS; c++)
            a = walk(board, r, c, depth, a);
    return a;
}

int main(void) {
    const int64_t depth = 25, total = 12, modulus = 1000000007;
    uint8_t **board = malloc(ROWS * sizeof(uint8_t *));
    for (int r = 0; r < ROWS; r++) {
        board[r] = malloc(COLS * sizeof(uint8_t));
        for (int c = 0; c < COLS; c++)
            board[r][c] = 'A';
    }
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t rr = search_all(board, depth, iter);
        sum = (sum + rr) % modulus;
    }
    printf("%lld\n", (long long)sum);
    for (int r = 0; r < ROWS; r++) free(board[r]);
    free(board);
    return 0;
}

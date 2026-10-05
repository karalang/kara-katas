// Benchmark workload for LeetCode #348 — C mirror of tic_tac_toe.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIDE 1000
#define GAMES 100

typedef struct {
    int64_t n;
    int64_t *rows;
    int64_t *cols;
    int64_t diag, anti;
} TicTacToe;

static TicTacToe ttt_new(int64_t n) {
    TicTacToe t = {n, calloc(n, sizeof(int64_t)), calloc(n, sizeof(int64_t)), 0, 0};
    return t;
}

static void ttt_free(TicTacToe *t) {
    free(t->rows);
    free(t->cols);
}

static int64_t make_move(TicTacToe *t, int64_t row, int64_t col, int64_t player) {
    int64_t d = player == 1 ? 1 : -1;
    t->rows[row] += d;
    t->cols[col] += d;
    if (row == col) t->diag += d;
    if (row + col == t->n - 1) t->anti += d;
    int64_t goal = d * t->n;
    if (t->rows[row] == goal || t->cols[col] == goal || t->diag == goal || t->anti == goal)
        return player;
    return 0;
}

int main(void) {
    int64_t cells = (int64_t)SIDE * SIDE;
    int64_t *order = malloc(sizeof(int64_t) * cells);
    for (int64_t c = 0; c < cells; c++) order[c] = c;
    int64_t x = 348;
    for (int64_t k = cells - 1; k > 0; k--) {
        x = (x * 1103515245 + 12345) % 2147483648;
        int64_t j = x / 16 % (k + 1);
        int64_t t = order[k];
        order[k] = order[j];
        order[j] = t;
    }

    int64_t sink = 0;
    for (int64_t g = 0; g < GAMES; g++) {
        int64_t start = g * cells / GAMES;
        TicTacToe game = ttt_new(SIDE);
        int64_t player = 1, moves = 0, winner = 0;
        while (moves < cells && winner == 0) {
            int64_t cell = order[(start + moves) % cells];
            winner = make_move(&game, cell / SIDE, cell % SIDE, player);
            moves++;
            player = 3 - player;
        }
        ttt_free(&game);
        sink = (sink * 31 + moves * (winner + 1)) % 1000000007;
    }
    free(order);
    printf("sink %lld\n", (long long)sink);
    return 0;
}

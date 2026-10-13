// Benchmark for #529: C mirror of the ★ arm (reveal recursively); see
// update_board.kara. The same seeded generator, so the same boards and
// clicks; a fresh copy of the board per click, as the ★ arm's clone.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t m, n;
    char *cells;
} Board;

static char *at(Board *b, int64_t r, int64_t c) { return &b->cells[r * b->n + c]; }

static int64_t mines_around(Board *b, int64_t r, int64_t c) {
    int64_t count = 0;
    for (int64_t dr = -1; dr <= 1; dr++) {
        for (int64_t dc = -1; dc <= 1; dc++) {
            int64_t y = r + dr, x = c + dc;
            if ((dr != 0 || dc != 0) && y >= 0 && y < b->m && x >= 0 && x < b->n) {
                char v = *at(b, y, x);
                if (v == 'M' || v == 'X') count++;
            }
        }
    }
    return count;
}

static void reveal(Board *b, int64_t r, int64_t c) {
    if (*at(b, r, c) != 'E') return;
    int64_t count = mines_around(b, r, c);
    if (count > 0) {
        *at(b, r, c) = (char)(48 + count);
        return;
    }
    *at(b, r, c) = 'B';
    for (int64_t dr = -1; dr <= 1; dr++) {
        for (int64_t dc = -1; dc <= 1; dc++) {
            int64_t y = r + dr, x = c + dc;
            if (y >= 0 && y < b->m && x >= 0 && x < b->n) reveal(b, y, x);
        }
    }
}

static Board update_board(Board board, int64_t r, int64_t c) {
    if (*at(&board, r, c) == 'M') {
        *at(&board, r, c) = 'X';
    } else {
        reveal(&board, r, c);
    }
    return board;
}

static int64_t seed = 529;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    Board boards[50];
    for (int b = 0; b < 50; b++) {
        int64_t percent = next_random() % 21;
        boards[b].m = 50;
        boards[b].n = 50;
        boards[b].cells = malloc(50 * 50);
        for (int i = 0; i < 50 * 50; i++) boards[b].cells[i] = next_random() % 100 < percent ? 'M' : 'E';
    }
    int64_t opened = 0, exploded = 0, checksum = 0;
    for (int round = 0; round < 400; round++) {
        for (int b = 0; b < 50; b++) {
            int64_t r = next_random() % 50;
            int64_t c = next_random() % 50;
            Board copy = boards[b];
            copy.cells = malloc(copy.m * copy.n);
            memcpy(copy.cells, boards[b].cells, copy.m * copy.n);
            Board after = update_board(copy, r, c);
            int64_t shown = 0;
            for (int64_t i = 0; i < after.m * after.n; i++) {
                char ch = after.cells[i];
                if (ch == 'X') {
                    exploded++;
                } else if (ch != 'E' && ch != 'M') {
                    shown++;
                }
            }
            opened += shown;
            checksum = (checksum * 31 + shown) % 1000000007;
            free(after.cells);
        }
    }
    printf("50 boards of 50 by 50, 400 rounds of clicks: %lld opened, %lld exploded, checksum %lld\n",
           (long long)opened, (long long)exploded, (long long)checksum);
    for (int b = 0; b < 50; b++) free(boards[b].cells);
    return 0;
}

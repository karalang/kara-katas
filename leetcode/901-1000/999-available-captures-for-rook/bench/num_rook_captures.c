// Benchmark: LeetCode #999 Available Captures for Rook -- the ★ arm, a
// walk from the rook each way, on random 8 by 8 boards. Mirrors
// num_rook_captures.kara, .rs, .py and go-seq/. The board is LeetCode's
// C shape, `char **`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_rook_captures(char **board) {
    int64_t rr = 0, rc = 0;
    for (int64_t r = 0; r < 8; r++)
        for (int64_t c = 0; c < 8; c++)
            if (board[r][c] == 'R') {
                rr = r;
                rc = c;
            }
    static const int64_t dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int64_t captures = 0;
    for (int d = 0; d < 4; d++) {
        int64_t dr = dirs[d][0], dc = dirs[d][1];
        int64_t r = rr + dr, c = rc + dc;
        while (r >= 0 && r < 8 && c >= 0 && c < 8) {
            if (board[r][c] == 'p') {
                captures++;
                break;
            }
            if (board[r][c] == 'B') break;
            r += dr;
            c += dc;
        }
    }
    return captures;
}

static int64_t seed = 999;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 500000;
    // 20 boards, the rook on a random square and each other square a pawn
    // 4 times in 16 and a bishop 2 times in 16
    char **boards[20];
    for (int b = 0; b < 20; b++) {
        int64_t rook = next_random() % 64;
        boards[b] = malloc(8 * sizeof(char *));
        for (int r = 0; r < 8; r++) {
            boards[b][r] = malloc(8);
            for (int c = 0; c < 8; c++) {
                int64_t x = next_random() % 16;
                boards[b][r][c] = r * 8 + c == rook ? 'R' : x < 4 ? 'p' : x < 6 ? 'B' : '.';
            }
        }
    }
    int64_t captures = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t k = (r + i) % 20;
            int64_t got = num_rook_captures(boards[k]);
            captures += got;
            check = (check * 31 + got + 1) % 1000000007;
            // a pawn put on or taken off one square, so no board stays put
            int64_t s = (r * 13 + i * 5) % 64;
            char *cell = &boards[k][s / 8][s % 8];
            if (*cell == '.')
                *cell = 'p';
            else if (*cell == 'p')
                *cell = '.';
        }
    }
    printf("%lld rounds over 20 boards: %lld captures, checksum %lld\n", (long long)rounds,
           (long long)captures, (long long)check);
    return 0;
}

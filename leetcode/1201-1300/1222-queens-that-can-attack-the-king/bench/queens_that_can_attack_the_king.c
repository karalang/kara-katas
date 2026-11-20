// LeetCode #1222 bench, C mirror of the Kāra ★ arm: mark the queens on an
// 8 by 8 board, then walk out from the king in each of the eight
// directions, over 5000 random boards of 1 to 63 queens drawn once, 50
// passes; checksum of the attackers in the order found.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 1222;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t count;
    int64_t (*queens)[2];
    int64_t king[2];
} Board;

// The attackers into `out` as pairs, their number returned.
static int64_t queens_attackthe_king(const Board *b, int64_t (*out)[2]) {
    int board[8][8];
    memset(board, 0, sizeof board);
    for (int64_t i = 0; i < b->count; i++) {
        board[b->queens[i][0]][b->queens[i][1]] = 1;
    }
    int64_t n = 0;
    for (int64_t dx = -1; dx <= 1; dx++) {
        for (int64_t dy = -1; dy <= 1; dy++) {
            if (dx == 0 && dy == 0) {
                continue;
            }
            int64_t x = b->king[0] + dx, y = b->king[1] + dy;
            while (x >= 0 && x < 8 && y >= 0 && y < 8) {
                if (board[x][y]) {
                    out[n][0] = x;
                    out[n][1] = y;
                    n++;
                    break;
                }
                x += dx;
                y += dy;
            }
        }
    }
    return n;
}

int main(void) {
    static Board boards[5000];
    for (int i = 0; i < 5000; i++) {
        int64_t count = next_random() % 63 + 1;
        int64_t squares[64];
        for (int k = 0; k < 64; k++) {
            squares[k] = k;
        }
        for (int64_t k = 0; k < count + 1; k++) {
            int64_t j = k + next_random() % (64 - k);
            int64_t t = squares[k];
            squares[k] = squares[j];
            squares[j] = t;
        }
        boards[i].count = count;
        boards[i].queens = malloc(sizeof(int64_t[2]) * count);
        for (int64_t k = 0; k < count; k++) {
            boards[i].queens[k][0] = squares[k] / 8;
            boards[i].queens[k][1] = squares[k] % 8;
        }
        boards[i].king[0] = squares[count] / 8;
        boards[i].king[1] = squares[count] % 8;
    }
    int64_t total = 0, check = 0;
    int64_t out[8][2];
    for (int pass = 0; pass < 200; pass++) {
        for (int i = 0; i < 5000; i++) {
            int64_t n = queens_attackthe_king(&boards[i], out);
            total += n;
            for (int64_t a = 0; a < n; a++) {
                check = (check * 131 + out[a][0] * 8 + out[a][1] + 1) % 1000000007;
            }
        }
    }
    printf("5000 boards of 1 to 63 queens, 200 passes: attackers total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 5000; i++) {
        free(boards[i].queens);
    }
    return 0;
}

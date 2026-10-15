// LeetCode #688: Knight Probability in Chessboard -- the chances, forward.
// Bench.
//
// 60 queries, boards of 15 to 25 squares a side and 50 to 100 moves from
// a random start, are drawn once; then 50 rounds answer every query.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t DR[8] = {2, 1, -1, -2, -2, -1, 1, 2};
static const int64_t DC[8] = {1, 2, 2, 1, -1, -2, -2, -1};

static double knight_probability(int64_t n, int64_t k, int64_t row, int64_t column) {
    double *board = calloc((size_t)(n * n), sizeof(double));
    board[row * n + column] = 1.0;
    for (int64_t s = 0; s < k; s++) {
        double *next = calloc((size_t)(n * n), sizeof(double));
        for (int64_t r = 0; r < n; r++) {
            for (int64_t c = 0; c < n; c++) {
                double p = board[r * n + c];
                if (p > 0.0) {
                    for (int m = 0; m < 8; m++) {
                        int64_t r2 = r + DR[m];
                        int64_t c2 = c + DC[m];
                        if (r2 >= 0 && r2 < n && c2 >= 0 && c2 < n) {
                            next[r2 * n + c2] += p / 8.0;
                        }
                    }
                }
            }
        }
        free(board);
        board = next;
    }
    double total = 0.0;
    for (int64_t i = 0; i < n * n; i++) {
        total += board[i];
    }
    free(board);
    return total;
}

static int64_t seed = 688;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 60, rounds = 50;
    int64_t qs[60][4];
    for (int64_t q = 0; q < count; q++) {
        int64_t n = 15 + next_random() % 11;
        int64_t k = 50 + next_random() % 51;
        int64_t row = next_random() % n;
        int64_t column = next_random() % n;
        qs[q][0] = n;
        qs[q][1] = k;
        qs[q][2] = row;
        qs[q][3] = column;
    }
    double sum = 0.0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t q = 0; q < count; q++) {
            sum += knight_probability(qs[q][0], qs[q][1], qs[q][2], qs[q][3]);
        }
    }
    printf("%lld queries answered, sum %.6f\n", (long long)(count * rounds), sum);
    return 0;
}

// Benchmark for #782: Transform to Chessboard -- mirror of the ★ arm (the
// corner rule and two counts), with the same workload as the Kāra program.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t moves_to_chessboard(int64_t **board, int64_t n) {
    for (int64_t r = 0; r < n; r++)
        for (int64_t c = 0; c < n; c++)
            if ((board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c]) == 1) return -1;
    int64_t row_ones = 0, col_ones = 0, row_off = 0, col_off = 0;
    for (int64_t i = 0; i < n; i++) {
        row_ones += board[0][i];
        col_ones += board[i][0];
        if (board[i][0] == i % 2) row_off++;
        if (board[0][i] == i % 2) col_off++;
    }
    if (row_ones != n / 2 && row_ones != (n + 1) / 2) return -1;
    if (col_ones != n / 2 && col_ones != (n + 1) / 2) return -1;
    if (n % 2 == 1) {
        if (row_off % 2 == 1) row_off = n - row_off;
        if (col_off % 2 == 1) col_off = n - col_off;
    } else {
        if (n - row_off < row_off) row_off = n - row_off;
        if (n - col_off < col_off) col_off = n - col_off;
    }
    return (row_off + col_off) / 2;
}

static int64_t seed = 782;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 64, N = 30 };
    int64_t **boards[COUNT];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t row_of[N], col_of[N];
        for (int64_t i = 0; i < N; i++) row_of[i] = col_of[i] = i;
        for (int64_t i = N - 1; i > 0; i--) {
            int64_t j = next_random() % (i + 1), t = row_of[i];
            row_of[i] = row_of[j]; row_of[j] = t;
            j = next_random() % (i + 1); t = col_of[i];
            col_of[i] = col_of[j]; col_of[j] = t;
        }
        int64_t **board = malloc(N * sizeof(int64_t *));
        for (int64_t r = 0; r < N; r++) {
            board[r] = malloc(N * sizeof(int64_t));
            for (int64_t c = 0; c < N; c++) board[r][c] = (row_of[r] + col_of[c]) % 2;
        }
        if (g % 4 == 1) {
            int64_t r = next_random() % N, c = next_random() % N;
            board[r][c] = 1 - board[r][c];
        } else if (g % 4 == 3) {
            for (int64_t c = 0; c < N; c++) board[0][c] = next_random() % 2;
            for (int64_t r = 1; r < N; r++) {
                int64_t flip = next_random() % 2;
                for (int64_t c = 0; c < N; c++) board[r][c] = board[0][c] ^ flip;
            }
        }
        boards[g] = board;
    }
    int64_t solvable = 0, checksum = 0;
    for (int64_t round = 0; round < 2000000; round++) {
        int64_t g = (round * 7) % COUNT;
        int64_t answer = moves_to_chessboard(boards[g], N);
        if (answer >= 0) solvable++;
        checksum = (checksum * 31 + answer + 2 + g) % 1000000007;
    }
    printf("2000000 rounds of 30 x 30 boards: %lld solvable, checksum %lld\n", (long long)solvable, (long long)checksum);
    return 0;
}

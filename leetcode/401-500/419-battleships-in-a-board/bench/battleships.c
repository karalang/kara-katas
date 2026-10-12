// LeetCode #419: Battleships in a Board -- C mirror of battleships.kara
// (count the first cells). Usage: ./battleships [rounds]
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 200

static int64_t count_battleships(char board[N][N], int64_t rows, int64_t cols) {
    int64_t count = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if (board[r][c] == 'X' && (r == 0 || board[r - 1][c] != 'X') && (c == 0 || board[r][c - 1] != 'X')) {
                count += 1;
            }
        }
    }
    return count;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static bool clear(char board[N][N], int64_t r, int64_t c) {
    const int64_t dr[5] = {0, -1, 1, 0, 0}, dc[5] = {0, 0, 0, -1, 1};
    for (int k = 0; k < 5; k++) {
        int64_t rr = r + dr[k], cc = c + dc[k];
        if (rr >= 0 && rr < N && cc >= 0 && cc < N && board[rr][cc] == 'X') {
            return false;
        }
    }
    return true;
}

static char board[N][N];

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 20000;
    int64_t seed = 419;
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            board[r][c] = '.';
        }
    }
    for (int t = 0; t < 4000; t++) {
        int64_t length = 1 + step(&seed) % 4;
        bool across = step(&seed) % 2 == 0;
        int64_t r = step(&seed) % N;
        int64_t c = step(&seed) % N;
        int64_t dr = across ? 0 : 1, dc = across ? 1 : 0;
        bool fits = r + dr * (length - 1) < N && c + dc * (length - 1) < N;
        for (int64_t k = 0; k < length; k++) {
            if (fits && !clear(board, r + dr * k, c + dc * k)) {
                fits = false;
            }
        }
        if (fits) {
            for (int64_t k = 0; k < length; k++) {
                board[r + dr * k][c + dc * k] = 'X';
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t i = 0; i < rounds; i++) {
        int64_t r = step(&seed) % N;
        int64_t c = step(&seed) % N;
        if (board[r][c] == 'X') {
            board[r][c] = '.';
            if (!clear(board, r, c)) {
                board[r][c] = 'X';
            }
        } else if (clear(board, r, c)) {
            board[r][c] = 'X';
        }
        int64_t answer = count_battleships(board, N, N);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld rounds on a %dx%d board: total %lld, checksum %lld\n", (long long)rounds, N, N, (long long)total, (long long)checksum);
    return 0;
}

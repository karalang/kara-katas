// LeetCode #723: Candy Crush -- crushed cells marked by their sign.
// Benchmark mirror of the Kara star arm: each round marks every run of
// three across or down by negating its cells, then drops each column,
// until a round marks nothing; the board is crushed on a copy, held
// as one flat array of rows where the others use a vector of rows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { M = 50, N = 50, BOARDS = 40 };

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static void candy_crush(const int64_t *board, int64_t *b, int64_t m, int64_t n) {
    memcpy(b, board, m * n * sizeof(int64_t));
    int stable = 0;
    while (!stable) {
        stable = 1;
        for (int64_t r = 0; r < m; r++)
            for (int64_t c = 0; c < n - 2; c++) {
                int64_t v = abs64(b[r * n + c]);
                if (v != 0 && abs64(b[r * n + c + 1]) == v && abs64(b[r * n + c + 2]) == v) {
                    b[r * n + c] = b[r * n + c + 1] = b[r * n + c + 2] = -v;
                    stable = 0;
                }
            }
        for (int64_t r = 0; r < m - 2; r++)
            for (int64_t c = 0; c < n; c++) {
                int64_t v = abs64(b[r * n + c]);
                if (v != 0 && abs64(b[(r + 1) * n + c]) == v && abs64(b[(r + 2) * n + c]) == v) {
                    b[r * n + c] = b[(r + 1) * n + c] = b[(r + 2) * n + c] = -v;
                    stable = 0;
                }
            }
        for (int64_t c = 0; c < n; c++) {
            int64_t write = m - 1;
            for (int64_t r = m - 1; r >= 0; r--)
                if (b[r * n + c] > 0) b[(write--) * n + c] = b[r * n + c];
            while (write >= 0) b[(write--) * n + c] = 0;
        }
    }
}

int main(void) {
    int64_t seed = 723;
    static int64_t boards[BOARDS][M * N];
    for (int d = 0; d < BOARDS; d++)
        for (int i = 0; i < M * N; i++) boards[d][i] = 1 + next_random(&seed) % 5;
    int64_t sum = 0;
    for (int64_t round = 0; round < 100; round++)
        for (int64_t d = 0; d < BOARDS; d++) {
            int64_t r = (round * 7 + d) % 50, c = (round * 13 + d * 3) % 50;
            boards[d][r * N + c] = 1 + (boards[d][r * N + c] + round) % 5;
            int64_t *after = malloc(M * N * sizeof(int64_t));
            candy_crush(boards[d], after, M, N);
            for (int i = 0; i < M * N; i++) sum += after[i] == 0;
            free(after);
        }
    printf("100 rounds of 40 boards of 50 x 50: %lld empty cells\n", (long long)sum);
    return 0;
}

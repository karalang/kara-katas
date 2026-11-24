// LeetCode #1301 bench: the ★ arm (a table from the bottom-right corner
// back, each square holding the most points reaching it and how many paths
// collect that many) over 20 boards of 100 by 100 with obstacles 0 to 38 in
// 100, built once; then 150 passes, each setting one square of every board to
// an obstacle or a digit from the checksum so far, answering it, and folding
// the score and the count into the checksum. The board's rows are strings,
// copied into a grid of characters each call as the other languages do, and
// the tables are a fresh malloc per row.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void paths_with_max_score(char **board, int64_t n, int64_t out[2]) {
    char **grid = malloc(sizeof(char *) * n);
    int64_t **best = malloc(sizeof(int64_t *) * n), **ways = malloc(sizeof(int64_t *) * n);
    for (int64_t i = 0; i < n; i++) {
        grid[i] = malloc(n);
        memcpy(grid[i], board[i], n);
        best[i] = malloc(sizeof(int64_t) * n);
        ways[i] = calloc(n, sizeof(int64_t));
        for (int64_t j = 0; j < n; j++) best[i][j] = -1;
    }
    const int64_t modulus = 1000000007;
    best[n - 1][n - 1] = 0;
    ways[n - 1][n - 1] = 1;
    int64_t moves[3][2] = {{1, 0}, {0, 1}, {1, 1}};
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t j = n - 1; j >= 0; j--) {
            if (grid[i][j] == 'X' || (i == n - 1 && j == n - 1)) continue;
            int64_t top = -1, count = 0;
            for (int m = 0; m < 3; m++) {
                int64_t a = i + moves[m][0], b = j + moves[m][1];
                if (a < n && b < n && best[a][b] >= 0) {
                    if (best[a][b] > top) {
                        top = best[a][b];
                        count = ways[a][b];
                    } else if (best[a][b] == top) {
                        count = (count + ways[a][b]) % modulus;
                    }
                }
            }
            if (top >= 0) {
                char c = grid[i][j];
                int64_t points = (c >= '0' && c <= '9') ? c - '0' : 0;
                best[i][j] = top + points;
                ways[i][j] = count;
            }
        }
    }
    if (best[0][0] < 0) {
        out[0] = 0;
        out[1] = 0;
    } else {
        out[0] = best[0][0];
        out[1] = ways[0][0];
    }
    for (int64_t i = 0; i < n; i++) {
        free(grid[i]);
        free(best[i]);
        free(ways[i]);
    }
    free(grid);
    free(best);
    free(ways);
}

static int64_t seed = 1301;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char **boards[20];
    for (int64_t t = 0; t < 20; t++) {
        int64_t wall = 2 * t;
        boards[t] = malloc(sizeof(char *) * 100);
        for (int i = 0; i < 100; i++) {
            boards[t][i] = malloc(101);
            for (int j = 0; j < 100; j++) {
                if (i == 0 && j == 0) boards[t][i][j] = 'E';
                else if (i == 99 && j == 99) boards[t][i][j] = 'S';
                else if (next_random() % 100 < wall) boards[t][i][j] = 'X';
                else boards[t][i][j] = (char)('0' + next_random() % 9 + 1);
            }
            boards[t][i][100] = 0;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 150; p++) {
        for (int t = 0; t < 20; t++) {
            int64_t at = 1 + check % 9998;
            int64_t i = at / 100, j = at % 100;
            boards[t][i][j] = check % 7 == 0 ? 'X' : (char)('0' + check % 9 + 1);
            int64_t got[2];
            paths_with_max_score(boards[t], 100, got);
            check = (check * 31 + got[0] + p) % 1000000007;
            check = (check * 31 + got[1]) % 1000000007;
        }
    }
    printf("150 passes over 20 boards of 100 by 100: checksum %lld\n", (long long)check);
    return 0;
}

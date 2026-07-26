/* Benchmark harness for LeetCode #130 — Surrounded Regions.
 * Mirrors surrounded_regions.kara algorithm-for-algorithm.
 *
 * The board is a genuinely nested structure (array of row pointers), not a
 * single flat block, matching the Vec<Vec<i64>> / [][]int64 the other lanes
 * use. A flat rows*cols array would give C a locality advantage the others do
 * not have.
 */

#include <stdio.h>
#include <stdlib.h>

#define ROWS 300
#define COLS 300
#define ITERS 400

static long long *pristine[ROWS];
static long long *work[ROWS];
static long long stack_[ROWS * COLS * 4];

static void flood(long long **board, long long rows, long long cols, long long sr, long long sc) {
    long long sp = 0;
    stack_[sp++] = sr * cols + sc;
    while (sp > 0) {
        long long pos = stack_[--sp];
        long long r = pos / cols;
        long long c = pos % cols;
        if (board[r][c] == 1) {
            board[r][c] = 2;
            if (r + 1 < rows) {
                stack_[sp++] = (r + 1) * cols + c;
            }
            if (r - 1 >= 0) {
                stack_[sp++] = (r - 1) * cols + c;
            }
            if (c + 1 < cols) {
                stack_[sp++] = r * cols + (c + 1);
            }
            if (c - 1 >= 0) {
                stack_[sp++] = r * cols + (c - 1);
            }
        }
    }
}

static void solve(long long **board, long long rows, long long cols) {
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            int on_border = (r == 0 || r == rows - 1 || c == 0 || c == cols - 1);
            if (on_border && board[r][c] == 1) {
                flood(board, rows, cols, r, c);
            }
        }
    }
    for (long long r = 0; r < rows; r++) {
        for (long long c = 0; c < cols; c++) {
            board[r][c] = (board[r][c] == 2) ? 1 : 0;
        }
    }
}

int main(void) {
    long long x = 5;
    for (long long r = 0; r < ROWS; r++) {
        pristine[r] = malloc(sizeof(long long) * COLS);
        work[r] = malloc(sizeof(long long) * COLS);
        for (long long c = 0; c < COLS; c++) {
            x = (x * 1103515245 + 12345) % 2147483648LL;
            pristine[r][c] = (x / 65536) % 2;
        }
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        for (long long a = 0; a < ROWS; a++) {
            for (long long b = 0; b < COLS; b++) {
                work[a][b] = pristine[a][b];
            }
        }

        solve(work, ROWS, COLS);

        long long h = 0;
        for (long long p = 0; p < ROWS; p++) {
            for (long long q = 0; q < COLS; q++) {
                h = (h * 31 + work[p][q]) % 1000000007LL;
            }
        }
        sink = (sink + h) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}

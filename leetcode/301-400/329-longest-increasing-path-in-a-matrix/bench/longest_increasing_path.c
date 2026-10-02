// Benchmark workload for LeetCode #329 — C mirror of
// longest_increasing_path.kara.
//
// Same workload: a SIDE x SIDE grid built once, then PUNCHES punches, each
// replacing one cell and finding the longest increasing path again with a
// fresh memo. Rows are separate allocations, as a Kāra Vec[Vec[i64]] is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIDE 500
#define PUNCHES 20
#define MODULUS 1073741789LL

static const int64_t DR[4] = {-1, 1, 0, 0};
static const int64_t DC[4] = {0, 0, -1, 1};

static int64_t longest_from(int64_t **matrix, int64_t **memo, int64_t rows, int64_t cols, int64_t r, int64_t c) {
    if (memo[r][c] > 0) {
        return memo[r][c];
    }
    int64_t here = matrix[r][c];
    int64_t best = 1;
    for (int k = 0; k < 4; k++) {
        int64_t nr = r + DR[k];
        int64_t nc = c + DC[k];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && matrix[nr][nc] > here) {
            int64_t len = 1 + longest_from(matrix, memo, rows, cols, nr, nc);
            if (len > best) {
                best = len;
            }
        }
    }
    memo[r][c] = best;
    return best;
}

static int64_t longest_increasing_path(int64_t **matrix, int64_t rows, int64_t cols) {
    if (rows == 0 || cols == 0) {
        return 0;
    }
    int64_t **memo = malloc(sizeof(int64_t *) * rows);
    for (int64_t r = 0; r < rows; r++) {
        memo[r] = calloc(cols, sizeof(int64_t));
    }
    int64_t best = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            int64_t len = longest_from(matrix, memo, rows, cols, r, c);
            if (len > best) {
                best = len;
            }
        }
    }
    for (int64_t r = 0; r < rows; r++) {
        free(memo[r]);
    }
    free(memo);
    return best;
}

static int64_t seed = 329;

static int64_t next_rand(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t **grid = malloc(sizeof(int64_t *) * SIDE);
    for (int64_t r = 0; r < SIDE; r++) {
        grid[r] = malloc(sizeof(int64_t) * SIDE);
        for (int64_t c = 0; c < SIDE; c++) {
            grid[r][c] = next_rand() % 1000;
        }
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t r = next_rand() % SIDE;
        int64_t c = next_rand() % SIDE;
        grid[r][c] = next_rand() % 1000;
        int64_t len = longest_increasing_path(grid, SIDE, SIDE);
        sink = (sink * 31 + len * 1000003 + r * SIDE + c) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    return 0;
}

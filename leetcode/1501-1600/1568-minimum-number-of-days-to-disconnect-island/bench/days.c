// LeetCode #1568: Minimum Number of Days to Disconnect Island -- bench:
// the ★ arm (each land cell taken away in turn) over 20 grids of 30 by 30,
// built once, all land but for a water cell one time in 20; 5 passes, each
// first turning one cell of every grid over.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 30

typedef struct { int64_t r, c; } Cell;

static int64_t islands(int64_t grid[N][N], int64_t rows, int64_t cols) {
    static unsigned char seen[N][N];
    static Cell stack[N * N];
    memset(seen, 0, sizeof seen);
    static const int64_t dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    int64_t count = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if (grid[r][c] == 1 && !seen[r][c]) {
                count++;
                seen[r][c] = 1;
                int64_t top = 0;
                stack[top++] = (Cell){r, c};
                while (top > 0) {
                    Cell at = stack[--top];
                    for (int k = 0; k < 4; k++) {
                        int64_t a = at.r + dr[k], b = at.c + dc[k];
                        if (a >= 0 && a < rows && b >= 0 && b < cols && grid[a][b] == 1 && !seen[a][b]) {
                            seen[a][b] = 1;
                            stack[top++] = (Cell){a, b};
                        }
                    }
                }
            }
        }
    }
    return count;
}

static int64_t min_days(int64_t source[N][N]) {
    if (islands(source, N, N) != 1) return 0;
    int64_t (*grid)[N] = malloc(sizeof(int64_t) * N * N);
    memcpy(grid, source, sizeof(int64_t) * N * N);
    int64_t answer = 2;
    for (int64_t r = 0; r < N && answer == 2; r++) {
        for (int64_t c = 0; c < N; c++) {
            if (grid[r][c] == 1) {
                grid[r][c] = 0;
                int split = islands(grid, N, N) != 1;
                grid[r][c] = 1;
                if (split) {
                    answer = 1;
                    break;
                }
            }
        }
    }
    free(grid);
    return answer;
}

static int64_t seed = 1568;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static int64_t grids[20][N][N];

int main(void) {
    const int64_t passes = 5;
    for (int g = 0; g < 20; g++)
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random() % 20 == 0 ? 0 : 1;
    int64_t check = 0, days[3] = {0, 0, 0};
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t g = 0; g < 20; g++) {
            int64_t at = (p * 7919 + g * 104729) % (N * N);
            grids[g][at / N][at % N] = 1 - grids[g][at / N][at % N];
            int64_t answer = min_days(grids[g]);
            days[answer]++;
            check = mix(check, answer);
        }
    }
    printf("%lld passes over 20 grids of 30 by 30: %lld need 0 days, %lld need 1, %lld need 2, checksum %lld\n",
           (long long)passes, (long long)days[0], (long long)days[1], (long long)days[2], (long long)check);
    return 0;
}

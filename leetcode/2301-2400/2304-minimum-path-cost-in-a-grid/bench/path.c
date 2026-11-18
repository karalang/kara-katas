// LeetCode #2304: Minimum Path Cost in a Grid -- the bench, the ★ arm in
// C. Row by row, each column of the next row takes the least over the
// row before of the cost so far plus the move, plus its own value.
#include <stdint.h>
#include <stdio.h>

enum { GRIDS = 20, M = 50, N = 50, CELLS = M * N };

static int64_t min_path_cost(const int64_t grid[M][N], const int64_t move_cost[CELLS][N]) {
    int64_t best[N], next[N];
    for (int j = 0; j < N; j++) best[j] = grid[0][j];
    for (int r = 1; r < M; r++) {
        for (int j = 0; j < N; j++) {
            int64_t least = INT64_MAX;
            for (int k = 0; k < N; k++) {
                int64_t c = best[k] + move_cost[grid[r - 1][k]][j];
                if (c < least) least = c;
            }
            next[j] = least + grid[r][j];
        }
        for (int j = 0; j < N; j++) best[j] = next[j];
    }
    int64_t least = best[0];
    for (int j = 1; j < N; j++)
        if (best[j] < least) least = best[j];
    return least;
}

static int64_t seed = 2304;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t grids[GRIDS][M][N];
    static int64_t tables[GRIDS][CELLS][N];
    for (int a = 0; a < GRIDS; a++) {
        int64_t values[CELLS];
        for (int64_t i = 0; i < CELLS; i++) values[i] = i;
        for (int64_t i = CELLS - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = values[i];
            values[i] = values[j];
            values[j] = t;
        }
        for (int r = 0; r < M; r++)
            for (int c = 0; c < N; c++) grids[a][r][c] = values[r * N + c];
        for (int v = 0; v < CELLS; v++)
            for (int j = 0; j < N; j++) tables[a][v][j] = next_random() % 100 + 1;
    }
    int64_t check = 0;
    for (int p = 0; p < 40; p++)
        for (int a = 0; a < GRIDS; a++)
            check = (check * 31 + min_path_cost(grids[a], tables[(a + p) % GRIDS])) % 1000000007;
    printf("40 passes over 20 grids of 50 by 50: checksum %lld\n", (long long)check);
    return 0;
}

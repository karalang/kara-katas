// LeetCode #1463 bench in C: the ★ arm (the most cherries over each pair of
// robot columns, row by row) on the same 40 grids of 70 by 70.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define R 70
#define W 70

static int cherry_pickup(int grid[R][W], int rows, int cols) {
    static int best[W][W], next[W][W];
    for (int a = 0; a < cols; a++)
        for (int b = 0; b < cols; b++) best[a][b] = -1;
    best[0][cols - 1] = grid[0][0] + grid[0][cols - 1];
    for (int r = 1; r < rows; r++) {
        for (int a = 0; a < cols; a++)
            for (int b = 0; b < cols; b++) next[a][b] = -1;
        for (int a = 0; a < cols; a++)
            for (int b = 0; b < cols; b++) {
                if (best[a][b] < 0) continue;
                for (int da = -1; da <= 1; da++)
                    for (int db = -1; db <= 1; db++) {
                        int x = a + da, y = b + db;
                        if (x < 0 || x >= cols || y < 0 || y >= cols) continue;
                        int here = x == y ? grid[r][x] : grid[r][x] + grid[r][y];
                        if (best[a][b] + here > next[x][y]) next[x][y] = best[a][b] + here;
                    }
            }
        memcpy(best, next, sizeof best);
    }
    int most = -1;
    for (int a = 0; a < cols; a++)
        for (int b = 0; b < cols; b++)
            if (best[a][b] > most) most = best[a][b];
    return most;
}

static int64_t seed = 1463;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int grids[40][R][W];
    for (int g = 0; g < 40; g++)
        for (int r = 0; r < R; r++)
            for (int c = 0; c < W; c++) grids[g][r][c] = (int)(next_random() % 101);
    int64_t check = 0;
    for (int g = 0; g < 40; g++) {
        int cell = (int)(check % 4900);
        grids[g][cell / 70][cell % 70] = (int)(check % 101);
        int64_t most = cherry_pickup(grids[g], R, W);
        check = (check * 31 + most) % 1000000007;
    }
    printf("40 grids of 70 by 70: checksum %lld\n", (long long)check);
    return 0;
}

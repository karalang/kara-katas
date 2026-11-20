// LeetCode #1254 bench, in C: the ★ arm (each island flooded to water by
// recursion from its first cell, and counted when no cell of it reached
// the edge) on 100 random 100 by 100 grids built once, each with its own
// share of land from 20 to 80 in 100; each copied and asked 40 times,
// every count folded into a checksum.

#include <stdio.h>
#include <string.h>

#define GRIDS 100
#define M 100
#define N 100

static long long seed = 1254;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int closed(long long grid[M][N], int i, int j) {
    if (i < 0 || j < 0 || i >= M || j >= N) return 0;
    if (grid[i][j] == 1) return 1;
    grid[i][j] = 1;
    int up = closed(grid, i - 1, j);
    int down = closed(grid, i + 1, j);
    int left = closed(grid, i, j - 1);
    int right = closed(grid, i, j + 1);
    return up && down && left && right;
}

static long long closed_island(long long grid[M][N]) {
    long long count = 0;
    for (int i = 0; i < M; i++)
        for (int j = 0; j < N; j++)
            if (grid[i][j] == 0 && closed(grid, i, j)) count++;
    return count;
}

static long long grids[GRIDS][M][N];
static long long work[M][N];

int main(void) {
    for (int g = 0; g < GRIDS; g++) {
        long long land = next_random() % 61 + 20;
        for (int i = 0; i < M; i++)
            for (int j = 0; j < N; j++) grids[g][i][j] = next_random() % 100 < land ? 0 : 1;
    }
    long long check = 0;
    for (int r = 0; r < 40; r++)
        for (int g = 0; g < GRIDS; g++) {
            memcpy(work, grids[g], sizeof work);
            check = (check * 131 + closed_island(work)) % 1000000007;
        }
    printf("40 rounds of 100 grids of 100 by 100: checksum %lld\n", check);
    return 0;
}

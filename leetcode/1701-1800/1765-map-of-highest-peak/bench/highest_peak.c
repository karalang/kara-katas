// LeetCode #1765: Map of Highest Peak -- the bench in C, mirroring
// highest_peak.kara: a breadth-first search from every water cell at once,
// the queue an array of cells as large as the grid.
#include <stdio.h>
#include <stdlib.h>

#define SIZE 800

static int **highest_peak(int **is_water, int rows, int cols) {
    int **height = malloc(sizeof(int *) * rows);
    for (int r = 0; r < rows; r++) {
        height[r] = malloc(sizeof(int) * cols);
        for (int c = 0; c < cols; c++) height[r][c] = -1;
    }
    long long *queue = malloc(sizeof(long long) * 2 * rows * cols);
    long long head = 0, tail = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (is_water[r][c] == 1) {
                height[r][c] = 0;
                queue[tail++] = r;
                queue[tail++] = c;
            }
        }
    }
    static const int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    while (head < tail) {
        long long r = queue[head++], c = queue[head++];
        for (int d = 0; d < 4; d++) {
            long long nr = r + dirs[d][0], nc = c + dirs[d][1];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && height[nr][nc] == -1) {
                height[nr][nc] = height[r][c] + 1;
                queue[tail++] = nr;
                queue[tail++] = nc;
            }
        }
    }
    free(queue);
    return height;
}

static long long seed = 1765;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int **grid = malloc(sizeof(int *) * SIZE);
    for (int r = 0; r < SIZE; r++) {
        grid[r] = malloc(sizeof(int) * SIZE);
        for (int c = 0; c < SIZE; c++) grid[r][c] = next_random() % 5000 == 0 ? 1 : 0;
    }
    grid[0][0] = 1;
    long long check = 0;
    for (long long call = 0; call < 100; call++) {
        long long r = (check + call * 7919) % SIZE;
        long long c = (check / 7 + call * 104729) % SIZE;
        grid[r][c] = 1 - grid[r][c];
        grid[0][0] = 1;
        int **height = highest_peak(grid, SIZE, SIZE);
        check = (check * 31 + height[c][r] + height[SIZE - 1 - r][SIZE - 1 - c]) % 1000000007;
        for (int i = 0; i < SIZE; i++) free(height[i]);
        free(height);
    }
    printf("100 calls on 800 by 800: checksum %lld\n", check);
    return 0;
}

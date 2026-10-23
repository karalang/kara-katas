// LeetCode #883 bench: C mirror of projection_area.kara (the ★ arm, one
// pass over rows and columns together) on the same 100 grids. The grid is
// an array of row pointers, as LeetCode passes it in C.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t projection_area(int64_t **grid, int64_t n) {
    int64_t area = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t row = 0, column = 0;
        for (int64_t j = 0; j < n; j++) {
            if (grid[i][j] > 0) area += 1;
            if (grid[i][j] > row) row = grid[i][j];
            if (grid[j][i] > column) column = grid[j][i];
        }
        area += row + column;
    }
    return area;
}

static int64_t seed = 883;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int g = 0; g < 100; g++) {
        // a grid of 40 x 40 to 50 x 50, towers up to 50, a quarter empty
        int64_t n = 40 + next_random() % 11;
        int64_t **grid = malloc(n * sizeof *grid);
        for (int64_t i = 0; i < n; i++) {
            grid[i] = malloc(n * sizeof **grid);
            for (int64_t j = 0; j < n; j++) {
                if (next_random() % 4 == 0) grid[i][j] = 0;
                else grid[i][j] = next_random() % 51;
            }
        }
        // 1000 towers rebuilt one at a time, the area after each
        for (int k = 0; k < 1000; k++) {
            int64_t i = next_random() % n;
            int64_t j = next_random() % n;
            grid[i][j] = next_random() % 51;
            int64_t area = projection_area(grid, n);
            total += area;
            check = (check * 131 + area) % 1000000007;
        }
        for (int64_t i = 0; i < n; i++) free(grid[i]);
        free(grid);
    }
    printf("100 grids, 1000 towers rebuilt in each: area %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}

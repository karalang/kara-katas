// Benchmark for #463: mirror of island_perimeter.kara (the ★ arm: four
// sides per land cell, less two per shared edge) on the same workload.
// A grid is an array of row pointers, like the Kāra Vec[Vec[i64]].
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t island_perimeter(int64_t **grid, int64_t rows, int64_t cols) {
    int64_t land = 0;
    int64_t shared = 0;
    for (int64_t i = 0; i < rows; i++) {
        for (int64_t j = 0; j < cols; j++) {
            if (grid[i][j] == 1) {
                land += 1;
                if (j + 1 < cols && grid[i][j + 1] == 1) {
                    shared += 1;
                }
                if (i + 1 < rows && grid[i + 1][j] == 1) {
                    shared += 1;
                }
            }
        }
    }
    return 4 * land - 2 * shared;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t **new_grid(int64_t rows, int64_t cols) {
    int64_t **grid = malloc(rows * sizeof(int64_t *));
    for (int64_t r = 0; r < rows; r++) {
        grid[r] = calloc(cols, sizeof(int64_t));
    }
    return grid;
}

static void free_grid(int64_t **grid, int64_t rows) {
    for (int64_t r = 0; r < rows; r++) {
        free(grid[r]);
    }
    free(grid);
}

// A random walk of land on a rows x cols sea, then every lake filled in.
static int64_t **random_island(int64_t rows, int64_t cols, int64_t steps, int64_t *seed) {
    int64_t **grid = new_grid(rows, cols);
    int64_t i = next_random(seed) % rows;
    int64_t j = next_random(seed) % cols;
    grid[i][j] = 1;
    for (int64_t s = 0; s < steps; s++) {
        int64_t d = next_random(seed) % 4;
        if (d == 0 && i > 0) {
            i -= 1;
        } else if (d == 1 && i + 1 < rows) {
            i += 1;
        } else if (d == 2 && j > 0) {
            j -= 1;
        } else if (d == 3 && j + 1 < cols) {
            j += 1;
        }
        grid[i][j] = 1;
    }
    int64_t **sea = new_grid(rows, cols);
    int64_t *queue = malloc(2 * rows * cols * sizeof(int64_t));
    int64_t len = 0;
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if ((r == 0 || c == 0 || r == rows - 1 || c == cols - 1) && grid[r][c] == 0) {
                sea[r][c] = 1;
                queue[2 * len] = r;
                queue[2 * len + 1] = c;
                len += 1;
            }
        }
    }
    static const int64_t dr[4] = {-1, 1, 0, 0};
    static const int64_t dc[4] = {0, 0, -1, 1};
    for (int64_t head = 0; head < len; head++) {
        int64_t r = queue[2 * head];
        int64_t c = queue[2 * head + 1];
        for (int k = 0; k < 4; k++) {
            int64_t nr = r + dr[k];
            int64_t nc = c + dc[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 0 && !sea[nr][nc]) {
                sea[nr][nc] = 1;
                queue[2 * len] = nr;
                queue[2 * len + 1] = nc;
                len += 1;
            }
        }
    }
    for (int64_t r = 0; r < rows; r++) {
        for (int64_t c = 0; c < cols; c++) {
            if (!sea[r][c]) {
                grid[r][c] = 1;
            }
        }
    }
    free(queue);
    free_grid(sea, rows);
    return grid;
}

int main(void) {
    const int64_t size = 1000;
    const int64_t islands = 2;
    const int64_t rounds = 200;
    int64_t seed = 463;
    int64_t **grids[2];
    int64_t tops[2];
    int64_t *shores[2];
    int64_t shore_len[2];
    for (int64_t g = 0; g < islands; g++) {
        int64_t **inner = random_island(size - 2, size - 2, (size - 2) * (size - 2), &seed);
        int64_t **grid = new_grid(size, size);
        for (int64_t r = 0; r < size - 2; r++) {
            for (int64_t c = 0; c < size - 2; c++) {
                grid[r + 1][c + 1] = inner[r][c];
            }
        }
        free_grid(inner, size - 2);
        int64_t top = 0;
        for (;;) {
            bool any = false;
            for (int64_t j = 0; j < size; j++) {
                any = any || grid[top][j] == 1;
            }
            if (any) {
                break;
            }
            top += 1;
        }
        shores[g] = malloc(size * sizeof(int64_t));
        shore_len[g] = 0;
        for (int64_t j = 0; j < size; j++) {
            if (grid[top][j] == 1) {
                shores[g][shore_len[g]++] = j;
            }
        }
        grids[g] = grid;
        tops[g] = top;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < islands; g++) {
            int64_t j = shores[g][next_random(&seed) % shore_len[g]];
            int64_t above = tops[g] - 1;
            grids[g][above][j] = 1;
            int64_t perimeter = island_perimeter(grids[g], size, size);
            grids[g][above][j] = 0;
            total += perimeter;
            checksum = (checksum * 31 + perimeter) % 1000000007;
        }
    }
    printf("%lld rounds on %lld islands of %lldx%lld: perimeter %lld in all, checksum %lld\n",
           (long long)rounds, (long long)islands, (long long)size, (long long)size, (long long)total,
           (long long)checksum);
    for (int64_t g = 0; g < islands; g++) {
        free_grid(grids[g], size);
        free(shores[g]);
    }
    return 0;
}

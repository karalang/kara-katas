// LeetCode #1030: Matrix Cells in Distance Order -- bench
// Mirrors ./cells_order.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t r_center, c_center;

static int64_t distance(const int64_t *cell) {
    return llabs(cell[0] - r_center) + llabs(cell[1] - c_center);
}

static int by_distance(const void *x, const void *y) {
    int64_t da = distance(x), db = distance(y);
    return (da > db) - (da < db);
}

// The answer as one malloc'd array of rows * cols pairs; the caller frees it.
static int64_t (*all_cells_dist_order(int rows, int cols, int64_t r0, int64_t c0))[2] {
    int64_t (*cells)[2] = malloc(sizeof(int64_t[2]) * rows * cols);
    int n = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            cells[n][0] = r;
            cells[n][1] = c;
            n++;
        }
    }
    r_center = r0;
    c_center = c0;
    qsort(cells, n, sizeof(int64_t[2]), by_distance);
    return cells;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 300;
    int64_t seed = 1030;
    int64_t centres[300][2];
    for (int k = 0; k < count; k++) {
        centres[k][0] = next_random(&seed) % 100;
        centres[k][1] = next_random(&seed) % 100;
    }
    int64_t total = 0, check = 0;
    for (int k = 0; k < count; k++) {
        int64_t r0 = centres[k][0], c0 = centres[k][1];
        int64_t (*cells)[2] = all_cells_dist_order(100, 100, r0, c0);
        int64_t weighted = 0;
        for (int i = 0; i < 100 * 100; i++) {
            weighted += (int64_t)(i + 1) * (llabs(cells[i][0] - r0) + llabs(cells[i][1] - c0));
        }
        free(cells);
        total += weighted;
        check = (check * 131 + weighted) % 1000000007;
    }
    printf("%d centres on a 100x100 grid: sum %lld, checksum %lld\n", count, (long long)total,
           (long long)check);
    return 0;
}

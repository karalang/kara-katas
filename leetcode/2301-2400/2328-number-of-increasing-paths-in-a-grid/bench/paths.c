// LeetCode #2328: Number of Increasing Paths in a Grid -- the bench, the
// ★ arm in C. The cells sorted by value, largest first, with `qsort`,
// and each cell's count of paths one plus its larger neighbours'
// counts, all of them already done. O(m n log(m n)).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL
#define ROWS 250
#define COLS 400

typedef struct { int64_t value, r, c; } Cell;

static int by_value_desc(const void *a, const void *b) {
    const Cell *x = a, *y = b;
    if (x->value != y->value) return x->value < y->value ? 1 : -1;
    if (x->r != y->r) return x->r < y->r ? 1 : -1;
    if (x->c != y->c) return x->c < y->c ? 1 : -1;
    return 0;
}

static int64_t count_paths(int64_t **grid, int64_t m, int64_t n) {
    Cell *cells = malloc(sizeof(Cell) * (size_t)(m * n));
    int64_t k = 0;
    for (int64_t r = 0; r < m; r++)
        for (int64_t c = 0; c < n; c++) cells[k++] = (Cell){grid[r][c], r, c};
    qsort(cells, (size_t)(m * n), sizeof(Cell), by_value_desc);
    static const int64_t moves[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    int64_t **from = malloc(sizeof(int64_t *) * (size_t)m);
    for (int64_t r = 0; r < m; r++) {
        from[r] = malloc(sizeof(int64_t) * (size_t)n);
        for (int64_t c = 0; c < n; c++) from[r][c] = 1;
    }
    int64_t total = 0;
    for (int64_t i = 0; i < m * n; i++) {
        int64_t value = cells[i].value, r = cells[i].r, c = cells[i].c;
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + moves[d][0], nc = c + moves[d][1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] > value)
                from[r][c] = (from[r][c] + from[nr][nc]) % MOD;
        }
        total = (total + from[r][c]) % MOD;
    }
    for (int64_t r = 0; r < m; r++) free(from[r]);
    free(from);
    free(cells);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2328;
    int64_t **grids[10];
    for (int k = 0; k < 10; k++) {
        grids[k] = malloc(sizeof(int64_t *) * ROWS);
        for (int r = 0; r < ROWS; r++) {
            grids[k][r] = malloc(sizeof(int64_t) * COLS);
            for (int c = 0; c < COLS; c++) grids[k][r][c] = next_random(&seed) % 1000 + 1;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 3; p++)
        for (int k = 0; k < 10; k++) check = (check * 31 + count_paths(grids[k], ROWS, COLS) + p) % 1000000007LL;
    printf("3 passes over 10 grids of 10^5 cells: checksum %lld\n", (long long)check);
    return 0;
}

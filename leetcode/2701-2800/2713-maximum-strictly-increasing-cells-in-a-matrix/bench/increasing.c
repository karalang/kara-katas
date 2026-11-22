// LeetCode #2713: Maximum Strictly Increasing Cells in a Matrix -- the
// bench (increasing.kara in C): the cells sorted by value, each value's
// cells answered from their row's and column's best before any is
// recorded.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t v, r, c; } Cell;

static int by_cell(const void *a, const void *b) {
    const Cell *x = a, *y = b;
    if (x->v != y->v) return x->v < y->v ? -1 : 1;
    if (x->r != y->r) return x->r < y->r ? -1 : 1;
    if (x->c != y->c) return x->c < y->c ? -1 : 1;
    return 0;
}

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t max_increasing_cells(const int64_t *mat, int64_t m, int64_t n) {
    Cell *cells = malloc(sizeof(Cell) * (size_t)(m * n));
    int64_t len = 0;
    for (int64_t r = 0; r < m; r++)
        for (int64_t c = 0; c < n; c++) cells[len++] = (Cell){mat[r * n + c], r, c};
    qsort(cells, (size_t)len, sizeof(Cell), by_cell);
    int64_t *row_best = calloc((size_t)m, sizeof(int64_t));
    int64_t *col_best = calloc((size_t)n, sizeof(int64_t));
    int64_t *found = malloc(sizeof(int64_t) * (size_t)len);
    int64_t best = 0;
    int64_t i = 0;
    while (i < len) {
        int64_t j = i;
        while (j < len && cells[j].v == cells[i].v) j++;
        for (int64_t k = i; k < j; k++)
            found[k - i] = max64(row_best[cells[k].r], col_best[cells[k].c]) + 1;
        for (int64_t k = i; k < j; k++) {
            int64_t r = cells[k].r, c = cells[k].c;
            row_best[r] = max64(row_best[r], found[k - i]);
            col_best[c] = max64(col_best[c], found[k - i]);
            best = max64(best, found[k - i]);
        }
        i = j;
    }
    free(cells);
    free(row_best);
    free(col_best);
    free(found);
    return best;
}

static int64_t seed = 2713;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 10, rounds = 10, side = 300;
    int64_t *mats = malloc(sizeof(int64_t) * (size_t)count * side * side);
    for (int k = 0; k < count; k++) {
        int64_t spread = next_random() % 9991 + 10;
        for (int i = 0; i < side * side; i++) mats[(size_t)k * side * side + i] = next_random() % spread;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t cells = max_increasing_cells(mats + (size_t)k * side * side, side, side);
            sum += cells;
            check = (check * 31 + cells + r) % 1000000007;
        }
    }
    printf("%d matrices of 300 by 300, %d rounds: cells sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(mats);
    return 0;
}

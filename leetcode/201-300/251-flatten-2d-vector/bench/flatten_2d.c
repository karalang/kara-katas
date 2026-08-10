// Benchmark workload for LeetCode #251 — Flatten 2D Vector (C mirror).
// Mirrors flatten_2d.kara algorithm-for-algorithm: same LCG, same ragged build,
// same lazy (row, col) iterator with skip-empty at both entry points.
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long **rows;
    long *lens;
    long nrows;
    long row;
    long col;
} Vector2D;

static void skip_empty(Vector2D *v) {
    while (v->row < v->nrows && v->col >= v->lens[v->row]) {
        v->row++;
        v->col = 0;
    }
}

static int v_has_next(Vector2D *v) {
    skip_empty(v);
    return v->row < v->nrows;
}

static long v_next(Vector2D *v) {
    skip_empty(v);
    if (v->row >= v->nrows) return -1;
    long x = v->rows[v->row][v->col];
    v->col++;
    return x;
}

int main(void) {
    long rows = 20000;
    long passes = 1500;

    long **data = malloc(rows * sizeof(long *));
    long *lens = malloc(rows * sizeof(long));
    long state = 251251;
    for (long r = 0; r < rows; r++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long n = 0;
        long *row = NULL;
        if ((state / 65536L) % 100L >= 45L) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            n = (state / 65536L) % 6L + 1L;
            row = malloc(n * sizeof(long));
            for (long c = 0; c < n; c++) {
                state = (state * 1103515245L + 12345L) & 2147483647L;
                row[c] = (state / 65536L) % 1000L;
            }
        }
        data[r] = row;
        lens[r] = n;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        Vector2D v = { data, lens, rows, 0, 0 };
        while (v_has_next(&v)) {
            long x = v_next(&v);
            sink = (sink * 31L + x + 1L) % 1000000007L;
        }
    }
    printf("%ld\n", sink);

    for (long r = 0; r < rows; r++) free(data[r]);
    free(data);
    free(lens);
    return 0;
}

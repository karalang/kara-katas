// Benchmark for #566: C mirror of the ★ arm (index arithmetic); see
// matrix_reshape.kara. A matrix is an array of `malloc`'d rows, and the
// reshaped matrix is fresh rows, as the Kāra arm's is fresh vectors; a
// shape that does not fit gives back a copy.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t rows;
    int64_t cols;
    int64_t **cells;
} Matrix;

static Matrix make(int64_t rows, int64_t cols) {
    Matrix m = {rows, cols, malloc(rows * sizeof(int64_t *))};
    for (int64_t i = 0; i < rows; i++) m.cells[i] = malloc(cols * sizeof(int64_t));
    return m;
}

static void release(Matrix m) {
    for (int64_t i = 0; i < m.rows; i++) free(m.cells[i]);
    free(m.cells);
}

static Matrix matrix_reshape(const Matrix *mat, int64_t r, int64_t c) {
    int64_t m = mat->rows;
    int64_t n = mat->cols;
    if (m * n != r * c) {
        Matrix copy = make(m, n);
        for (int64_t i = 0; i < m; i++) memcpy(copy.cells[i], mat->cells[i], n * sizeof(int64_t));
        return copy;
    }
    Matrix out = make(r, c);
    for (int64_t i = 0; i < r; i++) {
        for (int64_t j = 0; j < c; j++) {
            int64_t k = i * c + j;
            out.cells[i][j] = mat->cells[k / n][k % n];
        }
    }
    return out;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 800;
    int64_t shapes[10][2] = {{1, 10000}, {4, 2500}, {25, 400}, {50, 200}, {100, 100},
                             {200, 50},  {400, 25}, {2500, 4}, {10000, 1}, {99, 101}};
    int64_t seed = 566;
    Matrix *mats = malloc(count * sizeof(Matrix));
    for (int64_t g = 0; g < count; g++) {
        mats[g] = make(100, 100);
        for (int64_t i = 0; i < 100; i++)
            for (int64_t j = 0; j < 100; j++) mats[g].cells[i][j] = step(&seed) % 2001 - 1000;
    }
    int64_t cells = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t r = shapes[(round + g) % 10][0];
            int64_t c = shapes[(round + g) % 10][1];
            Matrix got = matrix_reshape(&mats[(round * 7 + g) % count], r, c);
            cells += got.rows * got.cols;
            checksum = (checksum * 31 + got.cells[round % got.rows][g % got.cols] + 1000) % 1000000007;
            release(got);
        }
    }
    printf("%lld matrices of 100 by 100, %lld rounds: %lld cells, checksum %lld\n", (long long)count,
           (long long)rounds, (long long)cells, (long long)checksum);
    for (int64_t g = 0; g < count; g++) release(mats[g]);
    free(mats);
    return 0;
}

// Benchmark for #562: C mirror of the ★ arm (one row of running counts);
// see longest_line.kara. Each row's three counts are fresh `calloc`'d
// arrays, as the Kāra arm's are fresh vectors.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t rows;
    int64_t cols;
    int64_t **cells;
} Matrix;

static int64_t max2(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t longest_line(const Matrix *mat) {
    int64_t n = mat->cols;
    int64_t *up = calloc(n, sizeof(int64_t));
    int64_t *diag = calloc(n, sizeof(int64_t));
    int64_t *anti = calloc(n, sizeof(int64_t));
    int64_t best = 0;
    for (int64_t i = 0; i < mat->rows; i++) {
        const int64_t *row = mat->cells[i];
        int64_t *next_up = calloc(n, sizeof(int64_t));
        int64_t *next_diag = calloc(n, sizeof(int64_t));
        int64_t *next_anti = calloc(n, sizeof(int64_t));
        int64_t across = 0;
        for (int64_t j = 0; j < n; j++) {
            if (row[j] == 1) {
                across += 1;
                next_up[j] = up[j] + 1;
                next_diag[j] = j > 0 ? diag[j - 1] + 1 : 1;
                next_anti[j] = j + 1 < n ? anti[j + 1] + 1 : 1;
                best = max2(max2(max2(max2(best, across), next_up[j]), next_diag[j]), next_anti[j]);
            } else {
                across = 0;
            }
        }
        free(up);
        free(diag);
        free(anti);
        up = next_up;
        diag = next_diag;
        anti = next_anti;
    }
    free(up);
    free(diag);
    free(anti);
    return best;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100;
    const int64_t rounds = 100;
    int64_t seed = 562;
    Matrix *matrices = malloc(count * sizeof(Matrix));
    int64_t m = 1;
    for (int64_t g = 0; g < count; g++) {
        int64_t percent = 50 + step(&seed) % 46;
        matrices[g].rows = m;
        matrices[g].cols = 10000 / m;
        matrices[g].cells = malloc(m * sizeof(int64_t *));
        for (int64_t i = 0; i < m; i++) {
            matrices[g].cells[i] = malloc(matrices[g].cols * sizeof(int64_t));
            for (int64_t j = 0; j < matrices[g].cols; j++) {
                matrices[g].cells[i][j] = step(&seed) % 100 < percent ? 1 : 0;
            }
        }
        m = m == 10000 ? 1 : m * 10;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t got = longest_line(&matrices[(round * 7 + g) % count]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld matrices of 10000 cells, %lld rounds: total %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < matrices[g].rows; i++) {
            free(matrices[g].cells[i]);
        }
        free(matrices[g].cells);
    }
    free(matrices);
    return 0;
}

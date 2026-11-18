// LeetCode #1605: Find Valid Matrix Given Row and Column Sums -- the bench
// in C, mirroring restore.kara: greedy, cell by cell in reading order,
// each row its own malloc.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int32_t **restore_matrix(const int32_t *row_sum, int64_t r, const int32_t *col_sum, int64_t c) {
    int32_t *rows = malloc(r * sizeof(int32_t));
    int32_t *cols = malloc(c * sizeof(int32_t));
    memcpy(rows, row_sum, r * sizeof(int32_t));
    memcpy(cols, col_sum, c * sizeof(int32_t));
    int32_t **m = malloc(r * sizeof(int32_t *));
    for (int64_t i = 0; i < r; i++) {
        int32_t *row = calloc(c, sizeof(int32_t));
        for (int64_t j = 0; j < c; j++) {
            int32_t x = rows[i] < cols[j] ? rows[i] : cols[j];
            row[j] = x;
            rows[i] -= x;
            cols[j] -= x;
        }
        m[i] = row;
    }
    free(rows);
    free(cols);
    return m;
}

static int64_t seed = 1605;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { P = 100, N = 1000 };
    int32_t *row_sums = calloc((size_t)P * N, sizeof(int32_t));
    int32_t *col_sums = calloc((size_t)P * N, sizeof(int32_t));
    for (int p = 0; p < P; p++)
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) {
                int32_t x = (int32_t)(next_random() % 1001);
                row_sums[p * N + i] += x;
                col_sums[p * N + j] += x;
            }
    int64_t check = 0, nonzero = 0;
    for (int p = 0; p < P; p++) {
        int32_t **m = restore_matrix(row_sums + p * N, N, col_sums + p * N, N);
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++)
                if (m[i][j] != 0) {
                    nonzero++;
                    check = (check * 31 + m[i][j] + 1) % 1000000007;
                }
            free(m[i]);
        }
        free(m);
    }
    printf("100 problems of 1000 by 1000: %lld cells not zero, checksum %lld\n", (long long)nonzero, (long long)check);
    free(row_sums);
    free(col_sums);
    return 0;
}

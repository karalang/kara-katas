/*
 * Benchmark workload — Set Matrix Zeroes (LeetCode #73).
 * C mirror of bench/set_matrix_zeroes.kara. Faithful to the kata's Vec-of-Vec
 * matrix: every row is a growable i64 buffer built by push (realloc doubling)
 * and the matrix itself is a growable buffer of row pointers — NOT a fixed 2-D
 * array — so the comparison measures the same growing-dynamic-array discipline
 * as Kāra's `Vec.new()+push` (the #72 fairness lesson). O(1)-space first-row/col
 * marker algorithm, K=100_000 iters over a 20×20 matrix with three punched zeros.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

/* Growable i64 vector (a matrix row). */
typedef struct { int64_t *data; int64_t len, cap; } Vec;
static Vec vec_new(void) { Vec v = {NULL, 0, 0}; return v; }
static void vpush(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 1;
        v->data = (int64_t *)realloc(v->data, sizeof(int64_t) * (size_t)v->cap);
    }
    v->data[v->len++] = x;
}

/* Growable vector of rows (the matrix). */
typedef struct { Vec *data; int64_t len, cap; } Mat;
static Mat mat_new(void) { Mat m = {NULL, 0, 0}; return m; }
static void mpush(Mat *m, Vec row) {
    if (m->len == m->cap) {
        m->cap = m->cap ? m->cap * 2 : 1;
        m->data = (Vec *)realloc(m->data, sizeof(Vec) * (size_t)m->cap);
    }
    m->data[m->len++] = row;
}
static void mat_free(Mat *m) {
    for (int64_t i = 0; i < m->len; i++) free(m->data[i].data);
    free(m->data);
}

static void set_zeroes(Mat *m) {
    int64_t rows = m->len;
    if (rows == 0) return;
    int64_t cols = m->data[0].len;

    int first_row_zero = 0, first_col_zero = 0;
    for (int64_t j = 0; j < cols; j++)
        if (m->data[0].data[j] == 0) first_row_zero = 1;
    for (int64_t i = 0; i < rows; i++)
        if (m->data[i].data[0] == 0) first_col_zero = 1;

    for (int64_t i = 1; i < rows; i++)
        for (int64_t j = 1; j < cols; j++)
            if (m->data[i].data[j] == 0) {
                m->data[i].data[0] = 0;
                m->data[0].data[j] = 0;
            }

    for (int64_t i = 1; i < rows; i++)
        for (int64_t j = 1; j < cols; j++)
            if (m->data[i].data[0] == 0 || m->data[0].data[j] == 0)
                m->data[i].data[j] = 0;

    if (first_row_zero)
        for (int64_t j = 0; j < cols; j++) m->data[0].data[j] = 0;
    if (first_col_zero)
        for (int64_t i = 0; i < rows; i++) m->data[i].data[0] = 0;
}

int main(void) {
    const int64_t total = 100000, modulus = 1000000007;
    const int64_t rows = 20, cols = 20;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        Mat m = mat_new();
        for (int64_t i = 0; i < rows; i++) {
            Vec row = vec_new();
            for (int64_t j = 0; j < cols; j++)
                vpush(&row, 1 + (i * 31 + j * 17 + k) % 9);
            mpush(&m, row);
        }
        m.data[k % rows].data[k % cols] = 0;
        m.data[(k * 7) % rows].data[(k * 13) % cols] = 0;
        m.data[(k * 3) % rows].data[(k * 11) % cols] = 0;

        set_zeroes(&m);

        for (int64_t i = 0; i < rows; i++)
            for (int64_t j = 0; j < cols; j++)
                acc = (acc * 131 + m.data[i].data[j]) % modulus;
        mat_free(&m);
    }
    printf("%lld\n", (long long)acc);
    return 0;
}

// Benchmark for #498: C mirror of the ★ arm (walking the zigzag); see
// diagonal_traverse.kara. Each matrix is an array of row pointers, as
// the ★ arm's is a Vec of rows, and each traversal grows a fresh output
// array by doubling, as a Vec does when pushed to.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t **rows;
    int64_t m, n;
} Matrix;

static int64_t *find_diagonal_order(const Matrix *mat, int64_t *len) {
    int64_t m = mat->m, n = mat->n;
    int64_t cap = 4, count = 0;
    int64_t *out = malloc(cap * sizeof(int64_t));
    int64_t r = 0, c = 0;
    int up = 1;
    while (count < m * n) {
        if (count == cap) {
            cap *= 2;
            out = realloc(out, cap * sizeof(int64_t));
        }
        out[count++] = mat->rows[r][c];
        if (up) {
            if (c == n - 1) {
                r++;
                up = 0;
            } else if (r == 0) {
                c++;
                up = 0;
            } else {
                r--;
                c++;
            }
        } else {
            if (r == m - 1) {
                c++;
                up = 1;
            } else if (c == 0) {
                r++;
                up = 1;
            } else {
                r++;
                c--;
            }
        }
    }
    *len = count;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 100 matrices of 10,000 cells (the problem's most), in ten shapes
    // from 1 by 10,000 to 10,000 by 1, with values from -100,000 to
    // 100,000, built once. Then each is traversed 100 times; every
    // traversal is folded into the checksum, each value weighed by its
    // place.
    static const int64_t rows[10] = {1, 4, 10, 25, 50, 100, 200, 400, 1000, 10000};
    static Matrix all[100];
    int64_t seed = 498;
    for (int k = 0; k < 100; k++) {
        int64_t m = rows[k % 10];
        int64_t n = 10000 / m;
        all[k].m = m;
        all[k].n = n;
        all[k].rows = malloc(m * sizeof(int64_t *));
        for (int64_t i = 0; i < m; i++) {
            all[k].rows[i] = malloc(n * sizeof(int64_t));
            for (int64_t j = 0; j < n; j++) {
                all[k].rows[i][j] = next_random(&seed) % 200001 - 100000;
            }
        }
    }
    int64_t checksum = 0;
    for (int t = 0; t < 100; t++) {
        for (int k = 0; k < 100; k++) {
            int64_t len;
            int64_t *order = find_diagonal_order(&all[k], &len);
            int64_t s = 0;
            for (int64_t i = 0; i < len; i++) {
                s += order[i] * (i % 7 + 1);
            }
            checksum = (checksum * 31 + s % 1000000007 + 1000000007) % 1000000007;
            free(order);
        }
    }
    printf("100 matrices of 10000 cells, 100 times each: checksum %lld\n", (long long)checksum);
    return 0;
}
